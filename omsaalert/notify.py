import email.mime.text
import logging
import smtplib
import subprocess

import omsaalert.config.email
import omsaalert.utility

_LOGGER = logging.getLogger(__name__)


class Notify(object):
    def send_emails(self, emails, problems):
        print("Notifying: {}".format(emails))

        content = omsaalert.utility.get_pretty_json(problems)

        m = email.mime.text.MIMEText(content)

        m["Subject"] = omsaalert.config.email.SUBJECT
        m["From"] = omsaalert.config.email.FROM_EMAIL
        m["To"] = ", ".join(emails)

        if omsaalert.config.email.SSL:
            s_class = smtplib.SMTP
        else:
            s_class = smtplib.SMTP_SSL
        s = s_class(
            omsaalert.config.email.SMTP_HOSTNAME,
            omsaalert.config.email.SMTP_PORT,
        )
        if omsaalert.config.email.USERNAME:
            s.login(
                omsaalert.config.email.USERNAME,
                omsaalert.config.email.PASSWORD,
            )
        s.sendmail(omsaalert.config.email.FROM_EMAIL, emails, m.as_string())

        s.quit()

    def invoke_command(self, command, problems, stdin=False):
        print("Command: {}".format(command))
        print("")

        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
        )

        if stdin is True:
            content = omsaalert.utility.get_pretty_json(problems)
            content = content.encode("utf8")
        else:
            content = None

        stdout, _ = p.communicate(input=content)
        stdout = stdout.decode("utf8")

        print(stdout)
        print("")
