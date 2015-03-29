import os
import cgi
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail

class MainPage(webapp.RequestHandler):
  def get(self):

    path = self.request.path
    
    temp = os.path.join(os.path.dirname(__file__), os.path.basename(path))
	
    if not temp.endswith('html') or not os.path.isfile(temp):
      temp = os.path.join(os.path.dirname(__file__),'index.html')
      
    template_values = {
      'companyaddress': "426 Clementi Ave 3, #06-508, Singapore 120426",
      'debug_message': "",
      'googleanalytics': """
          <script type="text/javascript">

          var _gaq = _gaq || [];
          _gaq.push(['_setAccount', 'UA-22577511-1']);
          _gaq.push(['_trackPageview']);
        
          (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();
        
          </script>"""
      }  

    self.response.out.write(template.render(temp, template_values))
    
class InquiryPost(webapp.RequestHandler):
  def post(self):
    
    person = cgi.escape(self.request.get('Salutation') + ' ' + self.request.get('Name'))
    message = mail.EmailMessage(sender='Webserver <kyawtun@smg-united.com>')
    message.subject = "[server] Inquiry from the web site"
    message.to = "inquiry@smg-united.com"
    message.body = 'Name: ' + person + "\n" + \
      'Email: ' + self.request.get('Email') + "\n" + \
      'Phone: ' + self.request.get('Phone') + "\n" + \
      'Address: ' + self.request.get('Address') + "\n" + \
      'Country: ' + self.request.get('Country') + "\n" + \
      self.request.get('Body')
    
    message.send()
    
    template_values = {'inquier': person}
    
    path = os.path.join(os.path.dirname(__file__),'contacts-sent.html')
    self.response.out.write(template.render(path, template_values))
    
application = webapp.WSGIApplication(
                                     [('/inquiry', InquiryPost),
                                     ('/.*', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()