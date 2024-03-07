class email:
    def __init__(self):
        self.html = "<html><body>"

    def introduction(self, introduction_text='Hi,'):
        self.html = self.html + f"{introduction_text}<br>"
        return self.html

    def body(self, body_introduction='', body_text=''):
        body_introduction = None if body_introduction is None else body_introduction
        b = f"<p>{body_text}</p>"
        self.html = self.html + b
        return self.html
    
    def embed_image(self, header='', image_path=None, alt='', width='300', height='300'):
        ext = (os.path.splitext(image_path)[1]).replace(".","")
        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode("utf-8")
        img = f'{header}<br> <img src="data:image/{ext};base64,%s"/ alt={alt} width={width} height={height}>' % encoded_image
        self.html = self.html + img
        return self.html
    
    def embed_table(self, header='', table=None):
        tbl = table.to_html() if isinstance(table, pd.DataFrame) else table.render()
        t = f"<br> {header}<br>{tbl}"
        self.html = self.html + t
        return self.html
    
    def compose_email(self, salutation = 'Regards,', signature='Name Here'):
        self.html = f"{self.html}<br>{salutation}<br>{signature}</body></html>"
        return self.html

    def outlook_send(self, recipients, subject, display_email=True, attachments=None):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = recipients
        mail.Subject = subject
        mail.HTMLBody = self.html

        # Loop through list of file paths to attach files
        if attachments is not None:
            for attachment in attachments:
                mail.Attachments.Add(attachment)
        else:
            pass
        
        mail.Display = display_email
        mail.Send()
        
        
