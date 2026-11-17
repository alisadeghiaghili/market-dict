using System;
using System.Threading.Tasks;
using MarketDict;

namespace MarketDict.Client.Demo
{
    internal class Program
    {
        static async Task Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Console.WriteLine("==================================================");
            Console.WriteLine("🚀 MarketDict C# (.NET) Client Demo");
            Console.WriteLine("==================================================\n");

            using var client = new MarketDictClient("http://localhost:5000/api/v1");

            try
            {
                // 1. Health & Statistics
                Console.WriteLine("1️⃣ Checking Service Health & Stats...");
                var health = await client.GetHealthAsync();
                Console.WriteLine($"   Status:      {health.Status}");
                Console.WriteLine($"   Total Terms: {health.TotalTerms}");
                Console.WriteLine($"   Database:    {health.Database}");

                var stats = await client.GetStatsAsync();
                Console.WriteLine($"   Categories:  {stats.TotalCategories}");
                Console.WriteLine($"   Formulas:    {stats.FormulasCount} quantitative formulas\n");

                // 2. Bilingual Search
                Console.WriteLine("2️⃣ Bilingual Search Query: 'نسبت شارپ' (Sharpe Ratio)...");
                var search = await client.SearchTermsAsync(query: "نسبت شارپ", limit: 3);
                foreach (var term in search.Data)
                {
                    Console.WriteLine($"   • {term.TermEn} ({term.TermFa}) - {term.CategoryIcon} {term.CategoryFa}");
                }
                Console.WriteLine();

                // 3. Autocomplete / Instant Suggestions (<5ms)
                Console.WriteLine("3️⃣ Autocomplete Suggestions for prefix: 'bit'...");
                var suggestions = await client.SuggestAsync("bit", limit: 4);
                foreach (var s in suggestions)
                {
                    Console.WriteLine($"   👉 [{s.Id}] {s.TermEn} -> {s.TermFa}");
                }
                Console.WriteLine();

                // 4. Term Details with Formula
                Console.WriteLine("4️⃣ Retrieving Term Details for 'sharperatio'...");
                var termDetail = await client.GetTermAsync("sharperatio");
                Console.WriteLine($"   English:  {termDetail.TermEn}");
                Console.WriteLine($"   Persian:  {termDetail.TermFa}");
                Console.WriteLine($"   Category: {termDetail.CategoryFa} ({termDetail.CategoryEn})");
                if (termDetail.Formula != null)
                {
                    Console.WriteLine($"   Formula (LaTeX):\n   {termDetail.Formula.FormulaEn}");
                }
                Console.WriteLine();

                // 5. Random Term of the Day
                Console.WriteLine("5️⃣ Getting Random Term of the Day...");
                var randomTerm = await client.GetRandomTermAsync(hasDeep: true);
                Console.WriteLine($"   🎲 {randomTerm.TermEn} | {randomTerm.TermFa}");
                if (!string.IsNullOrEmpty(randomTerm.DefinitionFa))
                {
                    int previewLen = Math.Min(120, randomTerm.DefinitionFa.Length);
                    Console.WriteLine($"   Definition: {randomTerm.DefinitionFa.Substring(0, previewLen)}...\n");
                }

                Console.WriteLine("==================================================");
                Console.WriteLine("✅ C# Client demo executed successfully!");
                Console.WriteLine("==================================================");
            }
            catch (MarketDictApiException ex)
            {
                Console.WriteLine($"⚠️ API Error (Status {ex.StatusCode}): {ex.Message}");
                Console.WriteLine($"Details: {ex.Details}");
                Console.WriteLine("\nMake sure 'python app.py' is running at http://localhost:5000!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"⚠️ General Error: {ex.Message}");
            }
        }
    }
}
