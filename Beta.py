from telethon import TelegramClient, functions, types
import os
import asyncio
import hashlib
import hmac
import re

# dont forget to look at 105 line and write your 2fa password
link = "https://t.me/$premcodescd714910211a1f4e284471870114a7fa_180f2912cf0d6cd657" #link to buy a stars or gift a premium
api_id = 22051826
api_hash = "713ee0c13c60e46ecf2f9c3af4a7694b"
phone = "+3584573988888" # phone number
client = TelegramClient("storse", api_id, api_hash)
client.session.set_dc(2, "149.154.167.40", 443)

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def get_slug(url: str) -> str:
    match = re.search(r"https://t\.me/\$?([a-zA-Z0-9_]+)", url)
    return match.group(1) if match else ""

def pbkdf2_hmac_sha512(password: bytes, salt: bytes, iterations: int, dklen: int) -> bytes:
    return hashlib.pbkdf2_hmac('sha512', password, salt, iterations, dklen)

def mod_pow(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)

def compute_k(p: int, g: int) -> int:
    return int.from_bytes(sha256(p.to_bytes(256, 'big') + g.to_bytes(256, 'big')), 'big')

def compute_u(g_a: int, g_b: int) -> int:
    return int.from_bytes(sha256(g_a.to_bytes(256, 'big') + g_b.to_bytes(256, 'big')), 'big')

def sh(data: bytes, salt: bytes) -> bytes:
    return sha256(salt + data + salt)

def ph1(password: str, salt1: bytes, salt2: bytes) -> bytes:
    return sh(sh(password.encode(), salt1), salt2)

def ph2(password: str, salt1: bytes, salt2: bytes) -> bytes:
    return sh(pbkdf2_hmac_sha512(ph1(password, salt1, salt2), salt1, 100000, 64), salt2)

def generate_client_parameters(password: str, algo, srp_B: int) -> dict:
    g = algo.g
    p = algo.p
    p = int.from_bytes(p, "big")
    
    salt1 = algo.salt1
    salt2 = algo.salt2
    
    k = compute_k(p, g)
    
    x = int.from_bytes(ph2(password, salt1, salt2), 'big')
    v = mod_pow(g, x, p)
    
    a = int.from_bytes(os.urandom(256), 'big') % p
    g_a = mod_pow(g, a, p)
    
    u = compute_u(g_a, srp_B)
    
    k_v = (k * v) % p
    t = (srp_B - k_v) % p
    s_a = mod_pow(t, a + u * x, p)
    k_a = sha256(s_a.to_bytes(256, 'big'))
    
    return {
        "g_a": g_a,
        "k_a": k_a
    }

async def get_new_tmp(p_obj: types.InputCheckPasswordSRP) -> types.account.TmpPassword:
    tmp = await client(functions.account.GetTmpPasswordRequest(password=p_obj, period=8500))
    return tmp

def compute_m1(algo, g_a: int, g_b: int, k_a: bytes) -> bytes:
    p = algo.p
    p = int.from_bytes(p, "big")
    g = algo.g
    salt1 = algo.salt1
    salt2 = algo.salt2
    
    h_xor = bytes(x ^ y for x, y in zip(sha256(p.to_bytes(256, 'big')), sha256(g.to_bytes(256, 'big'))))
    return sha256(h_xor + sha256(salt1) + sha256(salt2) + g_a.to_bytes(256, 'big') + g_b.to_bytes(256, 'big') + k_a)

async def calc():
    pa = await client(functions.account.GetPasswordRequest())
    ca = pa.current_algo
    srp_B = pa.srp_B
    srp_B = int.from_bytes(srp_B, "big")
    srpid = pa.srp_id
    
    slug = get_slug(link)

    params = generate_client_parameters(password, ca, srp_B)
    g_a = params["g_a"]
    k_a = params["k_a"]
    
    M1 = compute_m1(ca, g_a, srp_B, k_a)
    return g_a, M1, srpid, slug

async def xoxol():
    await client.start(phone)
    global password
    password = "amirali1390" # your password
    
    g_a, M1, srpid, slug = await calc()
    
    pwr = types.InputCheckPasswordSRP(srp_id=srpid, A=g_a.to_bytes(256, "big"), M1=M1)
    tmp = await get_new_tmp(pwr)
    tmp_pass = tmp.tmp_password
    
    while True:
        inv = types.InputInvoiceSlug(slug=slug)
        form = await client(functions.payments.GetPaymentFormRequest(invoice=inv))
        fid = form.form_id
        idd = form.saved_credentials[0].id
        
        try:
            credentials = types.InputPaymentCredentialsSaved(id=idd, tmp_password=tmp_pass)
        except:
            g_a, M1, srpid, slug = await calc()
            pwr = types.InputCheckPasswordSRP(srp_id=srpid, A=g_a.to_bytes(256, "big"), M1=M1)
            tmp = await get_new_tmp(pwr)
            tmp_pass = tmp.tmp_password
            credentials = types.InputPaymentCredentialsSaved(id=idd, tmp_password=tmp_pass)
        
        await client(functions.payments.SendPaymentFormRequest(form_id=fid, invoice=inv, credentials=credentials))
        # await asyncio.sleep(0.05)

async def main():
    for _ in range(101):
        await asyncio.gather(xoxol())

asyncio.run(main())
