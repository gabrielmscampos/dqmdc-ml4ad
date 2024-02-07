import 'bootstrap/dist/css/bootstrap.min.css'
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css'
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'
import 'react-toastify/dist/ReactToastify.css'

import React from 'react'

import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from 'react-oidc-context'
import { WebStorageStateStore } from 'oidc-client-ts'

import Root from './root'
import { OIDC_AUTHORITY, OIDC_CLIENT_ID, OIDC_SCOPE } from './config/env'

// Note on "redirect_uri"
// Why we are using the `redirect_uri` as {window.location.origin + '/'} ?
// In order to the redirect_uri not be hardcoded, we are splitting the CERN redirect location on-the-fly and transforming to the redirect_uri
// registered at applications-portal and triggering our onSigninCallback.

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider
      authority={OIDC_AUTHORITY}
      client_id={OIDC_CLIENT_ID}
      scope={OIDC_SCOPE}
      redirect_uri={window.location.origin + '/'} // Note on that above
      onSigninCallback={(_user) => {
        window.history.replaceState(
          {},
          document.title,
          window.location.pathname
        )
      }}
      userStore={new WebStorageStateStore({ store: window.localStorage })}
    >
      <BrowserRouter>
        <Root />
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
)
