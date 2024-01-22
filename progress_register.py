def register_log(text, first=False):
    # Registro de actividad
    mode = "w" if first else "a"
    log_file = open("./selenium_outputs/log.out", mode)
    log_file.write(text)
    log_file.close()

def register_progress(progress, maximum):
    # Registro de progreso
    progress_file = open("./selenium_outputs/progress.out", "w")
    progress_file.write(str(100*progress/maximum))
    progress_file.close()