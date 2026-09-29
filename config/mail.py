from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend


class PlainConsoleEmailBackend(ConsoleEmailBackend):
    """
    Console backend that prints the raw subject/body instead of the
    MIME-encoded message. Django's default mail policy soft wraps any line
    over 78 bytes with quotes-printable "=" breaks, which corrupts long links
    (e.g. password reset URLs)
    """

    def write_message(self, message):
        self.stream.write("To: %s\n" % ", ".join(message.to))
        self.stream.write("Subject: %s\n\n" % message.subject)
        self.stream.write("%s\n" % message.body)
        self.stream.write("-" * 79 + "\n")