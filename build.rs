use std::env;
use std::path::PathBuf;
use std::process::Command;

fn main() {
    // Native Render Rust deployments previously compiled stale embedded HTML.
    // Generate the complete static site before rustc reads src/assets.rs.
    for path in ["build_site.py", "sitegen", "public/assets", "public/manus-storage", "public/portal.js", "public/site.js", "public/refine.js", "public/v2.js", "tests/motion_v3_audit.py"] {
        println!("cargo:rerun-if-changed={}", path);
    }
    println!("cargo:rerun-if-env-changed=SITE_ORIGIN");
    println!("cargo:rerun-if-env-changed=ALLOW_INDEXING");
    println!("cargo:rerun-if-env-changed=RENDER_EXTERNAL_URL");
    println!("cargo:rerun-if-env-changed=RENDER_SERVICE_NAME");

    let root = PathBuf::from(env::var("CARGO_MANIFEST_DIR").expect("CARGO_MANIFEST_DIR"));
    let service = env::var("RENDER_SERVICE_NAME").unwrap_or_default();
    let external = env::var("RENDER_EXTERNAL_URL").unwrap_or_default();
    let preview = service.contains("preview") || external.contains("preview");
    let allow = env::var("ALLOW_INDEXING").unwrap_or_else(|_| if preview { "false".into() } else { "true".into() });
    let origin = env::var("SITE_ORIGIN").unwrap_or_else(|_| {
        if !external.is_empty() { external.clone() }
        else if allow.eq_ignore_ascii_case("true") { "https://mtassistant-oozm.onrender.com".into() }
        else { String::new() }
    });
    let python = if Command::new("python3").arg("--version").output().is_ok() { "python3" } else { "python" };
    let status = Command::new(python)
        .arg("build_site.py")
        .current_dir(&root)
        .env("SITE_ORIGIN", origin)
        .env("ALLOW_INDEXING", allow)
        .status()
        .expect("Static site build requires Python 3");
    assert!(status.success(), "御策靜態網站產生失敗");
    let audit = Command::new(python)
        .arg("tests/motion_v3_audit.py")
        .current_dir(&root)
        .status()
        .expect("V3 asset audit could not run");
    assert!(audit.success(), "御策 V3 影像與下載頁驗收失敗");
}
