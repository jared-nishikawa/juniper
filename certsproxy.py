import os
import subprocess

def __genPath(domain):
    return "./certs/" + domain

# Generate a certificate on the fly for a given domain
def genCert(domain):
    # first check to see if it already exists
    P = __genPath(domain)
    if os.path.isfile(P + '.crt'):
        return P + '.crt', P + '.key'

    # otherwise, generate a private key
    key = __genKey(domain)

    # Generate CSR
    __genCSR(domain)

    # Sign CSR with rootCA.key
    __signCSR(domain)

    # And return the new cert
    cert = P + '.crt'
    return cert,key 

# Sign CSR with rootCA.key
def __signCSR(domain):
    P = __genPath(domain)
    cmd = "openssl x509 -req -in " + P + \
            ".csr -CA ./certs/rootCA.pem -CAkey ./certs/rootCA.key " +\
            "-CAcreateserial -out " + P + ".crt -days 365 -sha256"
    proc = subprocess.Popen(cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    proc.wait()


# Generate a csr
def __genCSR(domain):
    P = __genPath(domain)
    # Prepare the stream to be sent in as stdin to the csr command
    info = "US\nColorado\nDenver\nSecureSet\nUnit\n" + \
            domain + "\njared@secureset.com\n\n\n"

    cmd = "openssl req -new -key " + P + ".key -out " + P + ".csr"
    proc = subprocess.Popen(cmd.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    proc.stdin.write(info)
    proc.wait()


# Generate a private key
def __genKey(domain):
    P = __genPath(domain)
    cmd = "openssl genrsa -out " + P + ".key 2048"
    proc = subprocess.Popen(cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    proc.wait()

    return P + '.key'
