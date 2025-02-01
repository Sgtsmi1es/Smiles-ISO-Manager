# ISO Organizer Docker
v0.0.2
A lightweight Docker container to organize ISO files on Unraid with a simple web portal.

## 🚀 Features
- Auto-organize ISOs by date and name
- Web interface for management (port 1337)
- Duplicate detection

## 🐳 Docker Usage
```bash
docker build -t iso-organizer .
docker run -d -p 1337:1337 -v /mnt/user/isos:/mnt/user/isos iso-organizer