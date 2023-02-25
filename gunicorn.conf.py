import multiprocessing

bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count()
accesslog = "/tmp/ocr.access.log"
wsgi_app  = "ocr:app"