'''
    Created By : Christian Merriman
    Date 3/27/26

    Purpose : I created some basic tests to make sure pages are working correctly with the etags I added.
    I also fake the time so I can simulate a file update, so it should reload the page and get the new etag.
'''
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch


#path used for our html files and etag checks
html_path = "ocp\\templates\\ocp"

class PageTests(TestCase):
    #test the index.html
    def test_index_page_status_code(self):
        #get the first load of the page
        url = reverse('index')

        #sim the file being created at time 1000.0
        with patch('os.path.getmtime') as mocked_mtime:
            mocked_mtime.return_value = 1000.0

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            #now test for etag load
            #get etag and make sure its not None
            etag = response.get('ETag')
            self.assertIsNotNone(etag)
            
            #will check to see if there is anything newer for us at this url by using the etag
            response_cached = self.client.get(url, HTTP_IF_NONE_MATCH=etag)

            #now make sure the server did not resend the data, no changes were made, so it should not.
            self.assertEqual(response_cached.status_code, 304)

        #now sim the file being updated to a new time
        with patch('os.path.getmtime') as mocked_mtime:
            mocked_mtime.return_value = 2000.0

            #send in the first etag with time of 1000
            response_updated = self.client.get(url, HTTP_IF_NONE_MATCH=etag)

            #server should notice it changed and send back 200
            self.assertEqual(response_updated.status_code, 200)
            
            #make sure our new etag is different
            new_etag = response_updated.get('ETag')
            self.assertNotEqual(etag, new_etag)

    #test our non-members html files
    def test_non_members_page_status_code(self):
        html_files = [
                        'about',
                        'comingsoon',
                        'currentproducts',
                        'employment',
                        'mission'
        ]
        
        for html in html_files:

            #get the first load of the page
            url = reverse(html)

            #sim the file being created at time 1000.0
            with patch('os.path.getmtime') as mocked_mtime:
                mocked_mtime.return_value = 1000.0

                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

                #now test for etag load
                #get etag and make sure its not None
                etag = response.get('ETag')
                self.assertIsNotNone(etag)
                
                #will check to see if there is anything newer for us at this url by using the etag
                response_cached = self.client.get(url, HTTP_IF_NONE_MATCH=etag)

                #now make sure the server did not resend the data, no changes were made, so it should not.
                self.assertEqual(response_cached.status_code, 304)

            #now sim the file being updated to a new time
            with patch('os.path.getmtime') as mocked_mtime:
                mocked_mtime.return_value = 2000.0

                #send in the first etag with time of 1000
                response_updated = self.client.get(url, HTTP_IF_NONE_MATCH=etag)

                #server should notice it changed and send back 200
                self.assertEqual(response_updated.status_code, 200)
                
                #make sure our new etag is different
                new_etag = response_updated.get('ETag')
                self.assertNotEqual(etag, new_etag)

    #check to make sure the pages are correct
    def test_non_members_page_integrity(self):
        html_files = {
                        'about' : 'ABOUT OMNI CONSUMER PRODUCTS',
                        'comingsoon' : 'FUTURE INITIATIVES',
                        'currentproducts' : 'CURRENT PRODUCT LINEUP',
                        'employment' : 'CAREERS AT OCP',
                        'mission' : 'OFFICE OF THE CHAIRMAN'
                       }
        
        for html, header_text in html_files.items():
            url = reverse(html)
            response = self.client.get(url)

            #check status
            self.assertEqual(response.status_code, 200)

            #check content for our headers text
            self.assertContains(response, header_text)

            #check the template and make sure we are loading the correct html files
            self.assertTemplateUsed(response, f"ocp/non-members/{html}.html")


    #test for 404
    def test_404_on_nonexistent_page(self):
        # Try a URL that isn't in your urls.py
        response = self.client.get('/this-page-does-not-exist/')
        
        self.assertEqual(response.status_code, 404)
