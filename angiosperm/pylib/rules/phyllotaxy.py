from angiosperm.pylib.rules.perianth_phyllotaxy import PerianthPhyllotaxy


def get_phyllotaxy(traits):
    found = {t._trait for t in traits}
    phyllotaxy = []

    if "perianth_phyllotaxy" not in found and "number_of_perianth_whorls" in found:
        phyllotaxy.append("0")

    if "perianth_phyllotaxy" not in found and "number_of_perianth_spirals" in found:
        phyllotaxy.append("1")

    if phyllotaxy:
        traits.append(
            PerianthPhyllotaxy(_trait="perianth_phyllotaxy", phyllotaxy=phyllotaxy)
        )
