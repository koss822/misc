def get_middle(s):
    elen = len(s)/2
    olen = int(round(len(s)/2))
    return s[(elen-1):(elen+1)] if len(s)%2 == 0 else s[olen:olen+1]