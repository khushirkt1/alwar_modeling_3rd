"""Colab set-up helpers: safe Drive mount, package install, MODFLOW 6."""
import importlib.util
import os
import shutil
import subprocess
import sys
import warnings

MOUNT_POINT = "/content/drive"

# pip name -> import name, where they differ
_IMPORT_NAME = {
    "python-docx": "docx", "pymupdf": "fitz", "PyMuPDF": "fitz", "opencv-python": "cv2",
    "pillow": "PIL", "scikit-learn": "sklearn", "netCDF4": "netCDF4", "pyshp": "shapefile",
}


def is_mounted():
    """True if Google Drive is mounted (checks the mount table as well as os.path.ismount)."""
    if os.path.ismount(MOUNT_POINT):
        return True
    try:
        with open("/proc/mounts") as f:
            return any(line.split()[1] == MOUNT_POINT for line in f if len(line.split()) > 1)
    except OSError:
        return False


def clean_mountpoint():
    """Remove EMPTY local folders left at /content/drive when Drive is not mounted.

    Such folders appear when a cell calls ``os.makedirs`` on a Drive path after a
    restart, and Colab then refuses to mount ("Mountpoint must not already contain
    files"). Only empty directories are removed; if any file is present this raises
    instead of deleting it. Does nothing when Drive is mounted.
    """
    if is_mounted() or not os.path.isdir(MOUNT_POINT):
        return 0
    files = [os.path.join(r, f) for r, _, fs in os.walk(MOUNT_POINT) for f in fs]
    if files:
        raise RuntimeError(
            f"{MOUNT_POINT} is not mounted but holds {len(files)} local file(s), e.g. {files[0]}. "
            "Move or delete them yourself, then mount Drive again.")
    removed = 0
    for root, dirs, _ in os.walk(MOUNT_POINT, topdown=False):
        for d in dirs:
            os.rmdir(os.path.join(root, d)); removed += 1
    return removed


def mount_drive():
    """Mount Google Drive only if it is not mounted yet (clears empty local leftovers first)."""
    if is_mounted():
        return True
    from google.colab import drive  # imported here so the module loads outside Colab
    clean_mountpoint()
    drive.mount(MOUNT_POINT)
    return is_mounted()


def pip_install(packages):
    """Install only the packages that cannot be imported yet. Returns the list installed."""
    missing = [p for p in packages
               if importlib.util.find_spec(_IMPORT_NAME.get(p, p).split("[")[0]) is None]
    if missing:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing], check=True)
    return missing


def install_modflow(bindir="/content/bin"):
    """Download the MODFLOW 6 executable (Colab's disk is reset every session)."""
    exe = shutil.which("mf6")
    if exe is None:
        pip_install(["flopy"])
        os.makedirs(bindir, exist_ok=True)
        subprocess.run(["get-modflow", "--subset", "mf6", bindir], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.environ["PATH"] = bindir + os.pathsep + os.environ["PATH"]
        exe = shutil.which("mf6")
    return exe


def setup(packages=(), modflow=False, apt=()):
    """One call at the top of every notebook.

    - hides the jupyter_client DeprecationWarning that floods Colab output
    - mounts Drive safely
    - installs missing pip packages (and apt packages such as ``tesseract-ocr``)
    - optionally installs MODFLOW 6
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    mount_drive()
    if apt:
        subprocess.run(["apt-get", "-qq", "install", "-y", *apt], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    installed = pip_install(list(packages))
    exe = install_modflow() if modflow else None
    from . import paths
    print("Drive mounted:", is_mounted(),
          "| project folder exists:", paths.GW.exists())
    if installed:
        print("Installed:", ", ".join(installed))
    if modflow:
        print("MODFLOW 6:", exe)
    return paths
