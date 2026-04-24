# PDF 引擎系统依赖
apk add --update gobject-introspection-dev cairo-dev pango-dev gdk-pixbuf-dev libffi-dev glib-dev font-noto-cjk font-noto fontconfig && fc-cache -f -v

# 项目依赖项
uv add markdown weasyprint pymdown-extensions
