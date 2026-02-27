import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify

from catalog.models import Product


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def humanize_filename(stem: str) -> str:
    # "lec_bag-01" -> "Lec Bag 01"
    s = stem.replace("_", " ").replace("-", " ").strip()
    s = " ".join(s.split())
    return s.title() if s else "Product"


def unique_slug(base_slug: str) -> str:
    slug = base_slug
    i = 2
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug


class Command(BaseCommand):
    help = "Rebuild Product rows from files in media/products (creates products with image, name, slug)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without writing to DB.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Limit number of files processed (0 = no limit).",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]

        media_root = Path(getattr(settings, "MEDIA_ROOT", "media"))
        products_dir = media_root / "products"

        if not products_dir.exists():
            self.stdout.write(self.style.ERROR(f"Not found: {products_dir}"))
            self.stdout.write(
                "Tip: ensure your images are inside media/products/")
            return

        files = sorted([p for p in products_dir.iterdir()
                       if p.is_file() and p.suffix.lower() in IMAGE_EXTS])

        if limit and limit > 0:
            files = files[:limit]

        if not files:
            self.stdout.write(self.style.WARNING(
                f"No images found in: {products_dir}"))
            return

        created = 0
        skipped = 0

        for p in files:
            stem = p.stem
            name = humanize_filename(stem)
            base = slugify(stem) or slugify(name) or "product"
            slug = unique_slug(base)

            # If an existing product already points to this exact image path, skip
            rel_path = f"products/{p.name}"
            if Product.objects.filter(image=rel_path).exists():
                skipped += 1
                continue

            msg = f"CREATE: name='{name}' slug='{slug}' image='{rel_path}'"
            if dry_run:
                self.stdout.write(msg)
                continue

            obj = Product(
                name=name,
                slug=slug,
                price=0,
                description_en="",
                description_es="",
                category=None,
            )
            obj.image.name = rel_path  # assigns without re-uploading
            obj.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created: {created} | Skipped: {skipped} | Total files: {len(files)}"))
