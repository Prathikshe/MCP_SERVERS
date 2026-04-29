# MCP_SERVERS

![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange)

---

A modular collection of MCP (Model Context Protocol) servers for building scalable, extensible integrations across APIs and applications. Designed for flexibility and community contributions, enabling developers to create, share, and reuse interoperable MCP-compatible services.

## 🔍 Why This Project?

Modern applications require integrating multiple APIs, handling authentication, and maintaining consistency across services. This repository helps by:

- ⚡ Standardizing API interactions using MCP
- 🔌 Enabling plug-and-play integrations
- 🤖 Making services AI-agent compatible
- 🧩 Promoting reusable and modular design
- 🚀 Reducing development effort and time

**Result:** Faster development, cleaner architecture, and easier scaling.

## 📦 Features

- Modular MCP server architecture
- Ready-to-use API integration examples
- Multi-app credential handling
- Async support for high performance
- Easily extensible tool system
- Developer-friendly structure

## 💡 Example MCP Tools

### List Available Apps
```python
list_whatsapp_profile()
```

## Send Text Message
```python
send_whatsapp_text(
    whatsapp_business_profile="example_app",
    to_phone_number="1234567890",
    message="Hello from MCP!"
)
```

## Send Template Message
```python
send_whatsapp_template(
    whatsapp_business_profile="example_app",
    to_phone_number="1234567890",
    template_name="sample_template",
    language_code="en"
)
```

## ⚙️ Installation

1. Clone Repository
```bash
git clone https://github.com/your-username/MCP_SERVERS.git
cd MCP_SERVERS
```
2. Install Dependencies
```bash
pip install -r requirements.txt
```
## 🔑 Configuration
Create a credentials.json file:
```
json
[
  {
    "whatsapp_business_profile": "app1",
    "phone_number_id": "your_phone_number_id",
    "api_access_token": "your_access_token"
  }
]
```
## ▶️ Run the Server
```bash
python server.py
```

# 🔌 How MCP Works

1. MCP server exposes tools
2. Client (AI / app) invokes tools
3. Server processes request
4. External API is called
5. Structured response is returned

## 🧱 Project Structure

```text
MCP_SERVERS/
│── server.py
│── credentials.json
│── requirements.txt
│── tools/
│── services/
```
## 🤝 Contributing

Contributions are welcome! 🎉

- Add new MCP server integrations
- Improve performance or structure
- Submit bug fixes
- Share new ideas

**Steps:**

1. Fork the repo
2. Create a branch (`feature/new-server`)
3. Commit changes
4. Open a Pull Request

## 🌱 Roadmap

- ✅ Core MCP server framework
- 🔜 More API integrations
- 🔜 Database-backed credentials
- 🔜 Docker support
- 🔜 Deployment templates

## 📄 License

MIT License © 2026

## ⭐ Support

If you find this useful:

- ⭐ Star the repo
- 🍴 Fork it
- 🧠 Contribute
