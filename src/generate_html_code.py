def generate_newsletter_html(newsletter_data):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Your Stock Newsletter</title>
    </head>
    <body style="margin:0; padding:0; font-family:Arial, sans-serif; background-color:#f5f5f5;">
      <table align="center" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:auto; background-color:#ffffff; padding:20px;">
        <tr>
          <td align="center" style="padding-bottom:20px;">
            <h2 style="margin:0; font-size:24px;">📈 Weekly Stock Newsletter</h2>
            <p style="font-size:14px; color:#666;">Latest news for your tracked stocks</p>
          </td>
        </tr>
    '''
    count = 0
    #print(newsletter_data)
    for item in newsletter_data[0]:
        if count == 1:
            html += f'''
            <tr>
            <td style="padding:10px 0; border-top:1px solid #e0e0e0;">
            <h3 style="margin:0 0 10px 0; color:#333;">${item["ticker"]}</h3>
            '''
            count = 0
        count += 1
        title = item["title"]
        description = item["description"]
        url = item["url"]
        html += f'''
        <p style="margin:0 0 5px;"><strong>•</strong> <a href="{url}" style="color:#1a73e8; text-decoration:none;">{title}</a></p>
        <p style="margin:0 0 15px; font-size:14px; color:#555;">{description}</p>
            '''

        html += '</td></tr>'

    html += '''
        <tr>
          <td align="center" style="padding-top:30px; font-size:12px; color:#aaa;">
            © 2025 StockSpam — <a href="https://unsubscribe-link.com" style="color:#aaa;">Unsubscribe</a>
          </td>
        </tr>
      </table>
    </body>
    </html>
    '''

    return html
