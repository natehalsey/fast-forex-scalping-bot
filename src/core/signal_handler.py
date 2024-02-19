import signal


def add_signal_handler(sign, func):
    def _handle_sigterm(sig, frame):
        return func

    signal.signal(sign, _handle_sigterm)
