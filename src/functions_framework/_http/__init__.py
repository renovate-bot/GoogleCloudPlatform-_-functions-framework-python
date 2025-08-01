# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask

from functions_framework._http.flask import FlaskApplication


class HTTPServer:
    def __init__(self, app, debug, **options):
        self.app = app
        self.debug = debug
        self.options = options

        if isinstance(app, Flask):
            if self.debug:
                self.server_class = FlaskApplication
            else:
                try:
                    from functions_framework._http.gunicorn import GunicornApplication

                    self.server_class = GunicornApplication
                except ImportError as e:
                    self.server_class = FlaskApplication
        else:  # pragma: no cover
            if self.debug:
                from functions_framework._http.asgi import StarletteApplication

                self.server_class = StarletteApplication
            else:
                try:
                    from functions_framework._http.gunicorn import UvicornApplication

                    self.server_class = UvicornApplication
                except ImportError as e:
                    from functions_framework._http.asgi import StarletteApplication

                    self.server_class = StarletteApplication

    def run(self, host, port):
        http_server = self.server_class(
            self.app, host, port, self.debug, **self.options
        )
        http_server.run()


def create_server(app, debug, **options):
    return HTTPServer(app, debug, **options)
