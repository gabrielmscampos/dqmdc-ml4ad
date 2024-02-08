import { User } from 'oidc-client-ts'

import { OIDC_PUBLIC_TOKEN_NS, OIDC_CONFIDENTIAL_TOKEN_NS } from '../config/env'

export const getUserToken = ({ type }) => {
  const item = type === 'confidential' ? OIDC_CONFIDENTIAL_TOKEN_NS : OIDC_PUBLIC_TOKEN_NS
  const oidcStorage = localStorage.getItem(item)
  if (!oidcStorage) {
    throw new Error('User is not authenticated!')
  }
  const user = User.fromStorageString(oidcStorage)
  return {
    tokenType: user.token_type,
    accessToken: user.access_token
  }
}
