/*# py-deutsch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# py-deutsch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with py-deutsch.  If not, see <http://www.gnu.org/licenses/>.
*/
// Author: Haitike & hkr91 (algui91@gmail.com)

#include <wx/wx.h>

class wxMainApp : public wxApp
{
    public:
		// function called at the application initialization
			virtual bool OnInit();
};

IMPLEMENT_APP(wxMainApp);

bool wxMainApp::OnInit()
{
	// create a new frame and set it as the top most application window
    SetTopWindow( new wxFrame( NULL, -1, wxT("Cpp-Deutsch"), wxDefaultPosition, wxSize( -1, -1) ) );

	// show main frame
    GetTopWindow()->Show();

	// enter the application's main loop
    return true;
}

