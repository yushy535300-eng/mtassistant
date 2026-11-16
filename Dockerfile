FROM rust:1.75-bookworm AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock build.rs ./
COPY sitegen ./sitegen
COPY public ./public
COPY docs ./docs
COPY tests ./tests
COPY build_site.py ./
COPY src ./src
RUN apt-get update && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*
ARG SITE_ORIGIN
ARG ALLOW_INDEXING=false
RUN SITE_ORIGIN="$SITE_ORIGIN" ALLOW_INDEXING="$ALLOW_INDEXING" cargo build --release --locked

FROM debian:bookworm-slim
WORKDIR /app
ARG ALLOW_INDEXING=false
COPY --from=builder /app/target/release/mtassistant-official /app/yuce-site
ENV PORT=3000
ENV ALLOW_INDEXING=${ALLOW_INDEXING}
EXPOSE 3000
CMD ["/app/yuce-site"]
