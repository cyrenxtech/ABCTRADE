// MARK: - MODELS
struct GoldResponse: Codable {
    let monthlyLevel, weeklyLevel, dailyLevel: String
    let entryAdvices: [EntryAdvice]
    let newsUpdates: [MajorNews]
    
    // Coach D Dynamic Fields (Optional to prevent crash)
    let date, monthContext, marketCondition, bullTrigger: String?
    let bearTrigger, intradayBehavior, htfPositioning, howToTreat: String?
    let sellZone1, sellTP1, sellTP2, sellExtension: String?
    let buyZone1, buyTP1, buyTP2, buyAcceptanceLevel, riskPercent: String?
}

// MARK: - TRADING ENGINE
class TradingEngine: ObservableObject {
    @Published var selectedPeriod = "15"
    @Published var isLoading = true
    @Published var lastUpdated = "Never"
    
    @Published var monthlyLevel = "..."
    @Published var weeklyLevel = "..."
    @Published var dailyLevel = "..."
    @Published var entryAdvices: [EntryAdvice] = []
    @Published var newsUpdates: [MajorNews] = []
    
    // The specific coach data storage
    @Published var coach: GoldResponse? 

    func loadLiveContent() async {
        guard let url = URL(string: "https://abctrade-2.onrender.com/newsletter") else { return }
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            let decoded = try JSONDecoder().decode(GoldResponse.self, from: data)
            
            await MainActor.run {
                self.coach = decoded // Store the full object
                self.monthlyLevel = decoded.monthlyLevel
                self.weeklyLevel = decoded.weeklyLevel
                self.dailyLevel = decoded.dailyLevel
                self.entryAdvices = decoded.entryAdvices
                self.newsUpdates = decoded.newsUpdates
                self.lastUpdated = Date().formatted(date: .omitted, time: .shortened)
                self.isLoading = false
            }
        } catch {
            print("Decoding Error: \(error)") // Check console for specific field errors
            await MainActor.run { self.isLoading = false }
        }
    }
}
