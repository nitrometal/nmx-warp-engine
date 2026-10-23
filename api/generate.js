export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { key } = req.body || {};
    if (!key) {
      return res.status(400).json({ error: 'Missing public key' });
    }

    const isoDate = new Date().toISOString();
    
    const regResp = await fetch('https://api.cloudflareclient.com/v0i1909051800/reg', {
      method: 'POST',
      headers: {
        'User-Agent': 'okhttp/3.12.1',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        install_id: '',
        tos: isoDate,
        key: key,
        fcm_token: '',
        type: 'ios',
        locale: 'en_US'
      })
    });

    const regJson = await regResp.json();
    if (!regJson.result || !regJson.result.token) {
      return res.status(500).json({ error: 'Registration failed', details: regJson });
    }

    const { id, token } = regJson.result;
    
    const patchResp = await fetch('https://api.cloudflareclient.com/v0i1909051800/reg/' + id, {
      method: 'PATCH',
      headers: {
        'User-Agent': 'okhttp/3.12.1',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify({ warp_enabled: true })
    });

    const patchJson = await patchResp.json();
    const config = patchJson?.result?.config;

    const v4 = config?.interface?.addresses?.v4 || '172.16.0.2';
    const v6 = config?.interface?.addresses?.v6 || '';
    const peerKey = config?.peers?.[0]?.public_key || 'bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=';

    return res.status(200).json({
      success: true,
      v4: v4,
      v6: v6,
      peer_key: peerKey
    });

  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
