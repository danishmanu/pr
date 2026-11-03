import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")
    print(f" * Starting PharmaCare Online Pharmacy Server on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
