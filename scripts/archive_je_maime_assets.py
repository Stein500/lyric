#!/usr/bin/env python3
"""Archive les bruts déjà poussés dans Git pour garder la livraison courante légère.

Les 30 PNG restent INTÉGRALEMENT dans le commit indiqué par archive_visuels.json.
Ils sont restitués à la demande dans work/out/ par resolve_asset, sans perte.
Usage : --archive pour sortir les bruts de l'arbre courant après leur sauvegarde.
        --restore pour vérifier et restituer tous les bruts dans le cache de travail.
"""
import argparse
import hashlib
import subprocess
from je_maime_common import *

BRANCH='arena/01a072d8-lyric'
PREFIX='projets/je_maime_tellement/assets/raw/portrait/'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--archive',action='store_true')
    group.add_argument('--restore',action='store_true')
    args=parser.parse_args()
    assets=assets_by_slot()
    assert sorted(assets)==list(range(30))
    if args.restore:
        for asset in assets.values():
            path=resolve_asset(asset['source_image'],asset['sha256'])
            print(path)
        return
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()==BRANCH
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/'+BRANCH],cwd=ROOT,text=True).split()[0]
    if remote!=commit:
        raise ValueError('Pousser le checkpoint complet avant archivage')
    records=[]
    for slot,asset in assets.items():
        rel=asset['source_image']
        if not rel.startswith(PREFIX) or not rel.endswith('.png'):
            raise ValueError('Fichier hors du périmètre des bruts générés')
        assert sha256(ROOT/rel)==asset['sha256']
        stored=subprocess.check_output(['git','show',f'{commit}:{rel}'],cwd=ROOT)
        if hashlib.sha256(stored).hexdigest()!=asset['sha256']:
            raise ValueError('Le brut ne correspond pas à sa sauvegarde Git')
        records.append({'slot':slot,'path':rel,'sha256':asset['sha256'],'bytes':len(stored)})
    dump(PROJECT/'archive_visuels.json',{
        'version':1,'commit':commit,'branch':BRANCH,'verified_remote_checkpoint':True,
        'reason':'Les bruts générés sont conservés dans le checkpoint distant, sans perte, afin que le patch courant privilégie le MP4 complet et le MP3 (budget de persistance).',
        'restore_command':'.venv/bin/python scripts/archive_je_maime_assets.py --restore',
        'restoration_directory':'work/out/je_maime_tellement/restored_assets',
        'total_bytes':sum(v['bytes'] for v in records),'assets':records,
    })
    subprocess.run(['git','rm','--']+[v['path'] for v in records],cwd=ROOT,check=True)
    print(f'{len(records)} bruts archivés sans perte dans le commit {commit}.')
    assert_sources_unchanged()


if __name__=='__main__':
    main()
