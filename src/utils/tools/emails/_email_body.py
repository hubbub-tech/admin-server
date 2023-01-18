class EmailBodyFormatter:

    def __init__(self):
        self.preview = None
        self.user = None
        self.introduction = None
        self.content = None
        self.conclusion = None
        self.optional = None

    def build(self):

        with open("src/templates/email.html", "r") as html:
            email_html = html.read()

            email_html_formatted = email_html.replace("{PREVIEW}", self.preview)
            email_html_formatted = email_html_formatted.replace("{USER}", self.user)

            email_html_formatted = email_html_formatted.replace("{INTRODUCTION}", self.introduction)
            email_html_formatted = email_html_formatted.replace("{CONTENT}", self.content)
            email_html_formatted = email_html_formatted.replace("{CONCLUSION}", self.conclusion)

            if self.optional:
                email_html_formatted = email_html_formatted.replace("{OPTIONAL}", self.optional)
            else:
                email_html_formatted = email_html_formatted.replace("{OPTIONAL}", "")

        return email_html_formatted

    def make_link(self, link, text):
        assert isinstance(link, str)
        assert isinstance(text, str)

        return f"<a href='{link}'>{text}</a>"



class EmailBodyMessenger:

    def __init__(self):
        self.subject = None
        self.to = None
        self.body = None
        self.error = None


    def to_dict(self):
        return self.__dict__


