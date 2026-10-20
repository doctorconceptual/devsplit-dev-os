"""Interpret PageSpeed responses without inferring missing measurements."""


def _metric(response, name):
    return response.get("loadingExperience", {}).get("metrics", {}).get(name, {})


def evaluate(check_id, payload):
    """Return a grounded result for one checklist API observation."""
    response = payload.get("response", payload)
    lab = response.get("lighthouseResult", {}).get("audits", {})
    fields = response.get("loadingExperience", {}).get("metrics", {})
    if check_id == 56:
        metric = _metric(response, "LARGEST_CONTENTFUL_PAINT_MS")
        if isinstance(metric.get("percentile"), (int, float)):
            value = metric["percentile"]
            return {"exists": "Y" if value > 4000 else "N", "confidence": "high",
                    "evidence": f"PageSpeed URL field p75 LCP={value:g} ms ({metric.get('category', 'uncategorized')}); threshold 4000 ms. Separate Lighthouse lab LCP={lab.get('largest-contentful-paint', {}).get('numericValue')}; field and lab populations differ."}
    if check_id == 57:
        metric = fields.get("CUMULATIVE_LAYOUT_SHIFT_SCORE", {})
        if isinstance(metric.get("percentile"), (int, float)):
            value = metric["percentile"] / 100
            lab_value = lab.get("cumulative-layout-shift", {}).get("numericValue")
            return {"exists": "Y" if value > 0.1 else "N", "confidence": "high",
                    "evidence": f"PageSpeed URL field p75 CLS={value:g} (API hundredths / 100); threshold 0.1. Separate Lighthouse lab CLS={lab_value}; lab and field populations differ."}
    if check_id == 58:
        audit = lab.get("total-byte-weight", {})
        score = audit.get("score")
        total = audit.get("numericValue")
        if isinstance(score, (int, float)) or isinstance(total, (int, float)):
            bad = (isinstance(score, (int, float)) and score < 0.9) or (isinstance(total, (int, float)) and total > 2_000_000)
            return {"exists": "Y" if bad else "N", "confidence": "high",
                    "evidence": f"PageSpeed Lighthouse image/page-weight audit score={score}; total transfer={total} bytes; display={audit.get('displayValue', 'not provided')}. This is an API delivery-weight signal, not an assumption that every image lacks lazy loading."}
    return {"exists": "unsure", "confidence": "low",
            "evidence": "PageSpeed does not provide a usable measurement for this observation."}
