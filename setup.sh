mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml

apt-get update -y
apt-get install -y python3-dev python3-pip
apt-get install -y tesseract-ocr tesseract-ocr-fra tesseract-ocr-nld
rm -rf /var/lib/apt/lists/*