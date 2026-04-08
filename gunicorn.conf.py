# Render startup reliability: do not preload app, so master binds port quickly.
preload_app = False

# Keep logs visible in Render dashboard.
accesslog = "-"
errorlog = "-"
loglevel = "debug"

# Conservative defaults for free instance.
workers = 1
timeout = 300
