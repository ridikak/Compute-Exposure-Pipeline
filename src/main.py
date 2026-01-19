import argparse
from . import extract, transform, features, anomalies, visualize

def run_all(use_synth: bool):
    extract.run(use_synthetic=use_synth)
    transform.run()
    features.run()
    anomalies.run()
    visualize.run()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["extract","transform","features","anomalies","visualize","all"], default="all")
    ap.add_argument("--synthetic", action="store_true", help="Use synthetic data instead of CSVs")
    args = ap.parse_args()

    if args.stage == "all":
        run_all(use_synth=args.synthetic)
    else:
        if args.stage == "extract":
            extract.run(use_synthetic=args.synthetic)
        elif args.stage == "transform":
            transform.run()
        elif args.stage == "features":
            features.run()
        elif args.stage == "anomalies":
            anomalies.run()
        elif args.stage == "visualize":
            visualize.run()
