use std::{env, process::Command};

fn main() {
    println!("cargo:rerun-if-changed=build_site.py");
    println!("cargo:rerun-if-changed=sitegen");
    println!("cargo:rerun-if-changed=public/v2.js");
    println!("cargo:rerun-if-env-changed=SITE_ORIGIN");
    println!("cargo:rerun-if-env-changed=ALLOW_INDEXING");
    println!("cargo:rerun-if-env-changed=RENDER_EXTERNAL_URL");
    let indexing = env::var("ALLOW_INDEXING").unwrap_or_else(|_| "false".into());
    let origin = env::var("SITE_ORIGIN").ok().filter(|s| !s.is_empty())
        .or_else(|| env::var("RENDER_EXTERNAL_URL").ok().filter(|s| !s.is_empty()))
        .unwrap_or_else(|| if indexing.eq_ignore_ascii_case("true") {
            "https://mtassistant-oozm.onrender.com".into()
        } else { String::new() });
    let status = Command::new("python3")
        .arg("build_site.py")
        .env("SITE_ORIGIN", origin)
        .env("ALLOW_INDEXING", indexing)
        .status()
        .expect("python3 is required to generate the website before compiling");
    assert!(status.success(), "Website generation failed");
}
