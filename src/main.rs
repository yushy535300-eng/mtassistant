mod assets;
use std::env;
use std::fs;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::Duration;

fn mime(path: &str) -> &'static str {
    if path.ends_with(".html") {
        "text/html; charset=utf-8"
    } else if path.ends_with(".css") {
        "text/css; charset=utf-8"
    } else if path.ends_with(".js") {
        "application/javascript; charset=utf-8"
    } else if path.ends_with(".png") {
        "image/png"
    } else if path.ends_with(".webp") {
        "image/webp"
    } else if path.ends_with(".jpg") {
        "image/jpeg"
    } else if path.ends_with(".mp4") {
        "video/mp4"
    } else if path.ends_with(".woff2") {
        "font/woff2"
    } else if path.ends_with(".svg") {
        "image/svg+xml"
    } else if path.ends_with(".json") {
        "application/json; charset=utf-8"
    } else if path.ends_with(".xml") {
        "application/xml; charset=utf-8"
    } else {
        "text/plain; charset=utf-8"
    }
}
fn parse_byte_range(value: &str, len: usize) -> Result<(usize, usize), ()> {
    if len == 0 { return Err(()); }
    let spec = value.strip_prefix("bytes=").ok_or(())?;
    if spec.contains(',') { return Err(()); }
    let (first, last) = spec.split_once('-').ok_or(())?;
    if first.is_empty() {
        let suffix = last.parse::<usize>().map_err(|_| ())?;
        if suffix == 0 { return Err(()); }
        let count = suffix.min(len);
        return Ok((len - count, len - 1));
    }
    let start = first.parse::<usize>().map_err(|_| ())?;
    if start >= len { return Err(()); }
    let end = if last.is_empty() { len - 1 } else { last.parse::<usize>().map_err(|_| ())?.min(len - 1) };
    if end < start { return Err(()); }
    Ok((start, end))
}
fn send(stream: &mut TcpStream, status: &str, mime: &str, bytes: &[u8], head: bool, extra: &str) {
    let headers = format!("HTTP/1.1 {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\nX-Content-Type-Options: nosniff\r\nReferrer-Policy: strict-origin-when-cross-origin\r\nPermissions-Policy: camera=(), microphone=(), geolocation=()\r\n{}\r\n", status, mime, bytes.len(), extra);
    let _ = stream.write_all(headers.as_bytes());
    if !head {
        let _ = stream.write_all(bytes);
    }
    let _ = stream.flush();
}
fn handle(mut stream: TcpStream) {
    let _ = stream.set_read_timeout(Some(Duration::from_secs(5)));
    let _ = stream.set_write_timeout(Some(Duration::from_secs(10)));
    let mut input = Vec::new();
    let mut buffer = [0u8; 2048];
    while input.len() < 8192 {
        match stream.read(&mut buffer) {
            Ok(0) | Err(_) => return,
            Ok(size) => {
                input.extend_from_slice(&buffer[..size]);
                if input.windows(4).any(|w| w == b"\r\n\r\n") {
                    break;
                }
            }
        }
    }
    if input.len() >= 8192 {
        send(
            &mut stream,
            "431 Request Header Fields Too Large",
            "text/plain",
            b"Request header too large",
            false,
            "Cache-Control: no-store\r\n",
        );
        return;
    }
    let request = String::from_utf8_lossy(&input);
    let mut words = request.lines().next().unwrap_or("").split_whitespace();
    let method = words.next().unwrap_or("");
    let target = words.next().unwrap_or("/");
    let accepts_gzip = request.lines().any(|line| {
        let lower = line.to_ascii_lowercase();
        lower.starts_with("accept-encoding:")
            && lower.contains("gzip")
            && !lower.contains("gzip;q=0")
    });
    let range_header = request.lines().find_map(|line| {
        let (name, value) = line.split_once(':')?;
        if name.eq_ignore_ascii_case("range") { Some(value.trim()) } else { None }
    });
    let (path, query) = target.split_once('?').unwrap_or((target, ""));
    let head = method == "HEAD";
    if method != "GET" && !head {
        send(
            &mut stream,
            "405 Method Not Allowed",
            "text/plain",
            b"Method Not Allowed",
            false,
            "Allow: GET, HEAD\r\nCache-Control: no-store\r\n",
        );
        return;
    }
    let canonical_alias = match path {
        "/index.html" => Some("/"),
        "/mt" => Some("/features"),
        "/features/" => Some("/features"),
        "/auto/" => Some("/auto"),
        "/guide/" => Some("/guide"),
        "/download/" => Some("/download"),
        "/faq/" => Some("/faq"),
        "/contact/" => Some("/contact"),
        "/articles/" => Some("/articles"),
        _ => None,
    };
    if let Some(destination) = canonical_alias {
        let location = if query.is_empty() { destination.to_string() } else { format!("{}?{}", destination, query) };
        send(&mut stream, "301 Moved Permanently", "text/plain", b"", head,
            &format!("Location: {}\r\nCache-Control: public, max-age=300\r\n", location));
        return;
    }
    if [
        "/guide/matrix",
        "/guide/matrix/",
        "/guide/auto",
        "/guide/auto/",
    ]
    .contains(&path)
    {
        let destination = if path.starts_with("/guide/auto") {
            "/guide?system=auto"
        } else {
            "/guide?system=matrix"
        };
        send(
            &mut stream,
            "301 Moved Permanently",
            "text/plain",
            b"",
            head,
            &format!(
                "Location: {}\r\nCache-Control: public, max-age=120\r\n",
                destination
            ),
        );
        return;
    }
    if path == "/healthz" {
        send(
            &mut stream,
            "200 OK",
            "text/plain",
            b"ok",
            head,
            "Cache-Control: no-store\r\n",
        );
        return;
    }
    let selected = match path {
        "/" | "/index.html" => "/index.html",
        "/features" | "/features/" | "/mt" => "/pages/features.html",
        "/auto" | "/auto/" => "/pages/auto.html",
        "/guide" | "/guide/" => {
            if query.split('&').any(|p| p == "system=auto") {
                "/pages/guide-auto.html"
            } else {
                "/pages/guide.html"
            }
        }
        "/download" | "/download/" => "/pages/download.html",
        "/faq" | "/faq/" => "/pages/faq.html",
        "/contact" | "/contact/" => "/pages/contact.html",
        "/articles" => "/pages/articles.html",
        "/articles/matrix-workflow" => "/pages/article-matrix-workflow.html",
        "/articles/auto-checklist" => "/pages/article-auto-checklist.html",
        "/articles/model-panels" => "/pages/article-model-panels.html",
        "/articles/mobile-home-screen" => "/pages/article-mobile-home-screen.html",
        "/articles/execution-status" => "/pages/article-execution-status.html",
        "/articles/connection-troubleshooting" => "/pages/article-connection-troubleshooting.html",
        "/favicon.png" | "/favicon.ico" => "/assets/baccarat-logo.png",
        _ => path,
    };
    let asset = if selected.contains("..") || selected.contains('%') || selected.contains('\\') {
        None
    } else {
        assets::ASSETS.iter().find(|(route, _)| *route == selected)
    };
    if let Some((_, embedded)) = asset {
        let compressed = if accepts_gzip {
            assets::GZIP_ASSETS
                .iter()
                .find(|(route, _)| *route == selected)
        } else {
            None
        };
        let content = compressed.map(|(_, bytes)| *bytes).unwrap_or(*embedded);
        let suffix = if compressed.is_some() { ".gz" } else { "" };
        let bytes = if env::var("DEV_FILES").ok().as_deref() == Some("true") {
            fs::read(format!("public{}{}", selected, suffix)).unwrap_or_else(|_| content.to_vec())
        } else {
            content.to_vec()
        };
        let indexing = match env::var("ALLOW_INDEXING") {
            Ok(value) => value.eq_ignore_ascii_case("true"),
            Err(_) => assets::ASSETS.iter().find(|(route, _)| *route == "/robots.txt")
                .map(|(_, bytes)| String::from_utf8_lossy(bytes).lines().any(|line| line.trim() == "Allow: /"))
                .unwrap_or(false),
        };
        let robots = if indexing {
            ""
        } else {
            "X-Robots-Tag: noindex, nofollow, noarchive\r\n"
        };
        let versioned = query.split('&').any(|part| {
            part.strip_prefix("v=")
                .map(|value| value.len() == 12 && value.chars().all(|ch| ch.is_ascii_hexdigit()))
                .unwrap_or(false)
        });
        let cache = if selected.ends_with(".html")
            || selected.ends_with(".txt")
            || selected.ends_with(".xml")
            || selected.ends_with(".json")
        {
            "no-store"
        } else if versioned || selected.starts_with("/manus-storage/async-images/") {
            "public, max-age=31536000, immutable"
        } else {
            "no-cache"
        };
        let encoding = if compressed.is_some() {
            "Content-Encoding: gzip\r\n"
        } else {
            ""
        };
        let common_headers = format!(
            "Cache-Control: {}\r\nVary: Accept-Encoding\r\n{}{}",
            cache, robots, encoding
        );
        if selected.ends_with(".mp4") {
            let total = bytes.len();
            if let Some(value) = range_header {
                match parse_byte_range(value, total) {
                    Ok((start, end)) => {
                        send(&mut stream, "206 Partial Content", mime(selected), &bytes[start..=end], head,
                            &format!("{}Accept-Ranges: bytes\r\nContent-Range: bytes {}-{}/{}\r\n", common_headers, start, end, total));
                    }
                    Err(_) => {
                        send(&mut stream, "416 Range Not Satisfiable", mime(selected), b"", head,
                            &format!("{}Accept-Ranges: bytes\r\nContent-Range: bytes */{}\r\n", common_headers, total));
                    }
                }
            } else {
                send(&mut stream, "200 OK", mime(selected), &bytes, head,
                    &format!("{}Accept-Ranges: bytes\r\n", common_headers));
            }
        } else {
            send(&mut stream, "200 OK", mime(selected), &bytes, head, &common_headers);
        }
    } else {
        let fallback = b"<!doctype html><html><head><meta name=\"robots\" content=\"noindex\"></head><body><main><h1>404</h1><a href=\"/\">Home</a></main></body></html>";
        let embedded = assets::ASSETS
            .iter()
            .find(|(route, _)| *route == "/pages/404.html")
            .map(|(_, bytes)| *bytes)
            .unwrap_or(fallback);
        let body = if env::var("DEV_FILES").ok().as_deref() == Some("true") {
            fs::read("public/pages/404.html").unwrap_or_else(|_| embedded.to_vec())
        } else {
            embedded.to_vec()
        };
        send(
            &mut stream,
            "404 Not Found",
            "text/html; charset=utf-8",
            &body,
            head,
            "Cache-Control: no-store\r\nX-Robots-Tag: noindex\r\n",
        );
    }
}
fn main() -> std::io::Result<()> {
    let port = env::var("PORT").unwrap_or_else(|_| "3000".to_string());
    let listener = TcpListener::bind(format!("0.0.0.0:{}", port))?;
    let (sender, receiver) = mpsc::sync_channel::<TcpStream>(128);
    let receiver = Arc::new(Mutex::new(receiver));
    for _ in 0..8 {
        let receiver = Arc::clone(&receiver);
        thread::spawn(move || loop {
            let stream = receiver.lock().unwrap().recv();
            match stream {
                Ok(stream) => handle(stream),
                Err(_) => break,
            }
        });
    }
    eprintln!("YUCE website listening on port {}", port);
    for stream in listener.incoming() {
        if let Ok(stream) = stream {
            if sender.send(stream).is_err() {
                break;
            }
        }
    }
    Ok(())
}
