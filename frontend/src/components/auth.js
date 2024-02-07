import React, { useEffect } from 'react'

import { useAuth } from 'react-oidc-context'
import { useNavigate } from 'react-router-dom'
import Modal from 'react-bootstrap/Modal'

const PrivateRoute = ({ roles, component: Component, ...props }) => {
  // Methods hasRealmRole and hasResourceRole inspired from keycloak-js
  // Src code: https://github.com/keycloak/keycloak/blob/main/js/libs/keycloak-js/src/keycloak.js

  const REDIRECT_TIMEOUT = 5000 // ms
  const navigate = useNavigate()
  const auth = useAuth()
  const kc = auth.user?.profile
  const clientId = auth.settings.client_id

  useEffect(() => {
    if (!isAuthorized(roles)) {
      setTimeout(() => navigate('/'), REDIRECT_TIMEOUT)
    }
  }, [roles])

  const hasRealmRole = (role) => {
    const access = kc.cern_roles
    return !!access && access.indexOf(role) >= 0
  }

  const hasResourceRole = ({ role, resource }) => {
    if (!kc.resource_access) {
      return false
    }
    const access = kc.resource_access[resource || clientId]
    return !!access && access.roles.indexOf(role) >= 0
  }

  const validateRoles = (roles) => {
    return roles.some(r => {
      const realm = hasRealmRole(r)
      const resource = hasResourceRole(r)
      return realm || resource
    })
  }

  const isAuthorized = (roles) => {
    return auth.isAuthenticated && (roles === undefined || validateRoles(roles))
  }

  return (
    isAuthorized(roles)
      ? (
      <Component {...props} />
        )
      : (
      <Modal show={true}>
        <Modal.Header>
          <Modal.Title>Permission denied</Modal.Title>
        </Modal.Header>
        <Modal.Body>{auth.isAuthenticated ? 'It seems you doesn\'t have the necessary role for accessing this resource, ask the administrator!' : 'You are not authenticated!'}</Modal.Body>
        <Modal.Footer>
          {`Redirecting to home in ${REDIRECT_TIMEOUT / 1000} seconds...`}
        </Modal.Footer>
      </Modal>
        )
  )
}

export default PrivateRoute
