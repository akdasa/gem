from gem.db import laws, sessions, proposals

with open('sessions.json', 'w') as file:
    for session in sessions.all():
        file.write(str(session))

with open('proposals.json', 'w') as file:
    for proposal in proposals.all():
        file.write(str(proposal))

with open('laws.json', 'w') as file:
    for law in laws.all():
        file.write(str(law))
