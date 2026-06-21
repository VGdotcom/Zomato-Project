"""Quick smoke test for Phase 1: load → preprocess → repository."""

import sys
import logging
from collections import Counter

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logging.basicConfig(level=logging.ERROR) # Only show errors to keep output clean

# Ensure src is importable
sys.path.insert(0, ".")

from src.data.repository import RestaurantRepository

def main():
    console = Console()
    repo = RestaurantRepository()
    
    with console.status("[bold green]Loading dataset..."):
        repo.load()

    all_recs = repo.get_all()
    rated = [r for r in all_recs if r.rating > 0]
    avg_rating = sum(r.rating for r in rated) / len(rated) if rated else 0

    # 1. Summary Panel
    summary_text = (
        f"Total restaurants: [cyan]{repo.count()}[/cyan]\n"
        f"Unique locations: [cyan]{len(repo.get_locations())}[/cyan]\n"
        f"Unique cuisines: [cyan]{len(repo.get_cuisines())}[/cyan]\n"
        f"Avg rating (rated): [cyan]{avg_rating:.2f}[/cyan] ({len(rated)} rated)"
    )
    console.print(Panel(summary_text, title="Dataset Summary", border_style="blue"))

    # 2. Restaurants Table
    table = Table(title="Sample Restaurants (Top 5)", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", style="bold")
    table.add_column("Location")
    table.add_column("Cuisines")
    table.add_column("Cost (₹)", justify="right")
    table.add_column("Tier")
    table.add_column("Rating", justify="right")
    table.add_column("Votes", justify="right")

    for r in all_recs[:5]:
        table.add_row(
            r.id,
            r.name,
            r.location,
            r.cuisines_display(),
            str(r.cost_for_two),
            r.budget_tier,
            str(r.rating),
            str(r.votes)
        )
    
    console.print(table)

    # 3. Distributions
    tier_dist = Counter(r.budget_tier for r in all_recs)
    dist_table = Table(title="Budget Tier Distribution", show_header=True)
    dist_table.add_column("Tier", style="cyan")
    dist_table.add_column("Count", justify="right")
    
    for tier, count in tier_dist.most_common():
        dist_table.add_row(tier, str(count))
        
    console.print(dist_table)
    
    console.print("\n[bold green]✅ Phase 1 smoke test passed![/bold green]")

if __name__ == "__main__":
    main()
