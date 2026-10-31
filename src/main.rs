use std::env;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;
use std::time::Duration;

const HTML: &str = include_str!("../public/index.html");
const CSS: &str = include_str!("../public/site.css");
const JS: &str = include_str!("../public/site.js");

fn handle(mut stream: TcpStream) {
    let _ = stream.set_read_timeout(Some(Duration::from_secs(5)));
    let _ = stream.set_write_timeout(Some(Duration::from_secs(5)));
    let mut input = [0u8; 8192];
    let size = match stream.read(&mut input) {
        Ok(size) if size > 0 => size,
        _ => return,
    };
    let request = String::from_utf8_lossy(&input[..size]);
    let first = request.lines().next().unwrap_or("");
    let mut words = first.split_whitespace();
    let method = words.next().unwrap_or("");
    let path = words.next().unwrap_or("/").split('?').next().unwrap_or("/");
    let head_only = method == "HEAD";
    let (status, mime, content): (&str, &str, &str) = if method != "GET" && !head_only {
        ("405 Method Not Allowed", "text/plain; charset=utf-8", "Method Not Allowed")
    } else {
        match path {
            "/" | "/index.html" | "/features" | "/mt" | "/auto" | "/guide" | "/faq" | "/contact" => {
                ("200 OK", "text/html; charset=utf-8", HTML)
            }
            "/site.css" => ("200 OK", "text/css; charset=utf-8", CSS),
            "/site.js" => ("200 OK", "application/javascript; charset=utf-8", JS),
            "/healthz" => ("200 OK", "text/plain; charset=utf-8", "ok"),
            "/robots.txt" => ("200 OK", "text/plain; charset=utf-8", "User-agent: *\nAllow: /\n"),
            _ => ("404 Not Found", "text/plain; charset=utf-8", "Not Found"),
        }
    };
    let body = if head_only { "" } else { content };
    let headers = format!(
        "HTTP/1.1 {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\nCache-Control: public, max-age=120\r\nX-Content-Type-Options: nosniff\r\nReferrer-Policy: strict-origin-when-cross-origin\r\nX-Frame-Options: SAMEORIGIN\r\n\r\n",
        status,
        mime,
        if head_only { content.as_bytes().len() } else { body.as_bytes().len() }
    );
    let _ = stream.write_all(headers.as_bytes());
    if !head_only {
        let _ = stream.write_all(body.as_bytes());
    }
    let _ = stream.flush();
}

fn main() -> std::io::Result<()> {
    let port = env::var("PORT").unwrap_or_else(|_| "10000".to_string());
    let bind = format!("0.0.0.0:{}", port);
    let listener = TcpListener::bind(&bind)?;
    eprintln!("MT MATRIX official site listening on {}", bind);
    for stream in listener.incoming() {
        match stream {
            Ok(s) => { thread::spawn(|| handle(s)); }
            Err(e) => eprintln!("connection error: {}", e),
        }
    }
    Ok(())
}
