async function authGuard(r) {
    let auth = r.headersIn['Authorization'];
  
    if (!auth) {
      r.return(401, 'Unauthorized, Token not found in header, please login first and get token');
      return;
    }
  
    let jwt_token = null;
  
    try {
      
      jwt_token = auth.split(' ')[1];
  
      if (!jwt_token) {
        r.return(401, 'Unauthorized, token must be present a space after Bearer <token>');
        return;
      }
  
      let response = await ngx.fetch(`http://172.17.0.1:8881/public/auth/token/info?access_token=${jwt_token}`);
      let data = await response.json();
  
      if (response.status === 200) {
        r.headersOut['X-Auth-User'] = data.data.username;
        r.headersOut['X-Auth-Id'] = data.data.account_id;
        r.headersOut['Exception-Message'] = "";
        r.headersOut['Exception-Code'] = "";
        r.return(200, 'OK');
        return;
      } 
      r.headersOut['Exception-Message'] = data.message;
      r.headersOut['Exception-Code'] = data.error_code;

      r.return(response.status, '');

    } catch (err) {
      r.return(500, 'Internal server error');
      return;
    }
  
  }
  
  export default { authGuard };
  