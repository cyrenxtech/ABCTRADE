import SwiftUI
import WebKit

// MARK: - MODELS
struct EntryAdvice: Identifiable, Codable {
    var id = UUID()
    let timeframe: String
    let buy: String
    let tp: String
    let sl: String
    
    // Add '?' to make these optional.
    let sell: String?
    let sellTP: String?
    let sellSL: String?
    
    let colorHex: String

    var color: Color {
        switch colorHex {
        case "green": return .green
        case "orange": return .orange
        case "blue": return .blue
        default: return .gray
        }
    }

    enum CodingKeys: String, CodingKey {
        case timeframe, buy, tp, sl, sell, sellTP, sellSL, colorHex
    }
}

struct MajorNews: Identifiable, Codable {
    var id = UUID()
    let title: String
    let impact: String
    let description: String

    enum CodingKeys: String, CodingKey {
        case title, impact, description
    }
}

struct GoldResponse: Codable {
    let monthlyLevel: String
    let weeklyLevel: String
    let dailyLevel: String
    let entryAdvices: [EntryAdvice]
    let newsUpdates: [MajorNews]
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
    
    @Published var showAlert = false
    @Published var alertMessage = ""

    func loadLiveContent() async {
        guard let url = URL(string: "https://abctrade-2.onrender.com/newsletter") else { return }

        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            let decoded = try JSONDecoder().decode(GoldResponse.self, from: data)
            
            await MainActor.run {
                self.monthlyLevel = decoded.monthlyLevel
                self.weeklyLevel = decoded.weeklyLevel
                self.dailyLevel = decoded.dailyLevel
                self.entryAdvices = decoded.entryAdvices
                self.newsUpdates = decoded.newsUpdates
                self.lastUpdated = Date().formatted(date: .omitted, time: .shortened)
                self.isLoading = false
                triggerHaptic()
            }
        } catch {
            print("Decoding Error: \(error)")
            await MainActor.run { self.isLoading = false }
        }
    }
    
    private func triggerHaptic() {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.success)
    }
}

// MARK: - DASHBOARD VIEW
struct EducationalDashboardView: View {
    @StateObject var engine = TradingEngine()

    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                VStack(alignment: .leading) {
                    Text("ABC GOLD LIVE").font(.title3.bold())
                    Text("Updated: \(engine.lastUpdated)").font(.system(size: 10)).foregroundColor(.gray)
                }
                Spacer()
                HStack(spacing: 4) {
                    Circle().fill(engine.isLoading ? .red : .green).frame(width: 8, height: 8)
                    Text(engine.isLoading ? "SYNCING" : "LIVE").font(.caption2).bold()
                }
                .padding(6)
                .background(Color.white.opacity(0.1))
                .cornerRadius(4)
            }
            .padding().background(Color.black).foregroundColor(.white)

            ScrollView {
                VStack(spacing: 18) {
                    // Timeframe Picker
                    Picker("TF", selection: $engine.selectedPeriod) {
                        Text("15M").tag("15"); Text("4H").tag("240"); Text("Daily").tag("D")
                    }.pickerStyle(.segmented).padding(.horizontal)

                    // Live Chart with Drawing Tools enabled
                    LiveGoldChart(interval: engine.selectedPeriod)
                        .frame(height: 450) // Increased height to accommodate the toolbar better
                        .cornerRadius(12).padding(.horizontal)

                    // KEY LIQUIDITY LEVELS
                    VStack(alignment: .leading, spacing: 10) {
                        Text("HORIZONTAL RAYS").font(.caption.bold()).foregroundColor(.gray)
                        LevelRow(title: "Monthly (PMH/L)", detail: engine.monthlyLevel, color: .red)
                        LevelRow(title: "Weekly (PWH/L)", detail: engine.weeklyLevel, color: .blue)
                        LevelRow(title: "Daily (PDH/L)", detail: engine.dailyLevel, color: .yellow)
                    }
                    .padding().background(Color.white.opacity(0.05)).cornerRadius(12).padding(.horizontal)

                    // ADVISED ENTRIES
                    VStack(alignment: .leading, spacing: 12) {
                        Text("ADVISED ENTRIES").font(.caption.bold()).foregroundColor(.purple)
                        if engine.isLoading && engine.entryAdvices.isEmpty { ProgressView().padding() }
                        ForEach(engine.entryAdvices) { advice in
                            AdviceCard(advice: advice)
                        }
                    }
                    .padding(.horizontal)

                    // COACH D DAILY ADVISE
                    VStack(alignment: .leading, spacing: 15) {
                        Text("🧠 COACH D DAILY ADVISE").font(.headline).foregroundColor(.yellow)
                        CoachSection(title: "1. Define the Range (CRT)", bodyText: "H4/Daily: We are in a 'Warsh Shock' expansion. \(engine.monthlyLevel)")
                        CoachSection(title: "2. Volume Profile (FRVP)", bodyText: "POC is sitting heavy near $4,850. Below POC = Discount.")
                    }
                    .padding().background(Color.white.opacity(0.05)).cornerRadius(12).padding(.horizontal)

                    // NEWS UPDATE SECTION
                    VStack(alignment: .leading, spacing: 15) {
                        Text("🌍 MAJOR NEWS UPDATE").font(.headline).foregroundColor(.cyan)
                        ForEach(engine.newsUpdates) { news in
                            VStack(alignment: .leading, spacing: 5) {
                                HStack {
                                    Text(news.title).font(.system(size: 14, weight: .bold))
                                    Spacer()
                                    Text(news.impact).font(.system(size: 10, weight: .black))
                                        .foregroundColor(news.impact == "BULLISH" ? .green : (news.impact == "BEARISH" ? .red : .gray))
                                }
                                Text(news.description).font(.system(size: 12)).foregroundColor(.gray)
                                Divider().background(Color.white.opacity(0.1))
                            }
                        }
                    }
                    .padding().background(Color.white.opacity(0.05)).cornerRadius(12).padding(.horizontal)
                    
                    // FOOTER
                    VStack(spacing: 8) {
                        Text("4Cs. Conviction + Commitment + Consistency = Cash Flow.")
                            .font(.system(size: 13, weight: .bold, design: .monospaced))
                            .foregroundColor(.gray)
                        
                        Text("Disclaimer: All information provided is for educational purposes only and does not constitute financial advice. Trading involves significant risk.")
                            .font(.system(size: 10)).foregroundColor(.gray.opacity(0.6)).multilineTextAlignment(.center).padding(.horizontal, 40)
                    }
                    .padding(.top, 10)
                }
                .padding(.bottom, 30)
            }
            .refreshable {
                await engine.loadLiveContent()
            }
        }
        .background(Color.black.edgesIgnoringSafeArea(.all)).preferredColorScheme(.dark)
        .onAppear {
            Task { await engine.loadLiveContent() }
        }
    }
}

// MARK: - COMPONENTS
struct AdviceCard: View {
    let advice: EntryAdvice
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(advice.timeframe).font(.system(size: 14, weight: .black))
                .padding(.horizontal, 8).padding(.vertical, 4)
                .background(advice.color.opacity(0.3)).cornerRadius(4)

            HStack(spacing: 12) {
                VStack(alignment: .leading) {
                    Text("BUY ZONE").font(.system(size: 8, weight: .bold)).foregroundColor(.green)
                    Text(advice.buy).font(.system(size: 14, weight: .bold))
                }
                Spacer()
                LevelBox(label: "TP", value: advice.tp, color: .white)
                LevelBox(label: "SL", value: advice.sl, color: .red.opacity(0.8))
            }
            .padding(10).background(Color.green.opacity(0.05)).cornerRadius(8)

            if let sellPrice = advice.sell, let sTP = advice.sellTP, let sSL = advice.sellSL {
                HStack(spacing: 12) {
                    VStack(alignment: .leading) {
                        Text("SELL ZONE").font(.system(size: 8, weight: .bold)).foregroundColor(.red)
                        Text(sellPrice).font(.system(size: 14, weight: .bold))
                    }
                    Spacer()
                    LevelBox(label: "TP", value: sTP, color: .white)
                    LevelBox(label: "SL", value: sSL, color: .red.opacity(0.8))
                }
                .padding(10).background(Color.red.opacity(0.05)).cornerRadius(8)
            }
        }
        .padding(12).background(Color.white.opacity(0.03)).cornerRadius(12)
    }
}

struct LevelBox: View {
    let label: String; let value: String; let color: Color
    var body: some View {
        VStack(alignment: .leading) {
            Text(label).font(.system(size: 9)).foregroundColor(.gray)
            Text(value).font(.system(size: 12, weight: .bold)).foregroundColor(color)
        }
    }
}

struct LevelRow: View {
    let title: String; let detail: String; let color: Color
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(title).font(.system(size: 11, weight: .bold)).foregroundColor(color)
                Text(detail).font(.system(size: 13, weight: .medium)).foregroundColor(.white)
            }
            Spacer()
        }
    }
}

struct CoachSection: View {
    let title: String; let bodyText: String
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).font(.system(size: 14, weight: .bold)).foregroundColor(.white)
            Text(bodyText).font(.system(size: 13)).foregroundColor(.gray).lineLimit(nil)
        }
    }
}

// MARK: - UPDATED CHART WITH DRAWING TOOLS
struct LiveGoldChart: UIViewRepresentable {
    let interval: String
    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        webView.isOpaque = false
        webView.backgroundColor = .black
        return webView
    }
    
    func updateUIView(_ uiView: WKWebView, context: Context) {
        // 'hide_side_toolbar' is now FALSE and 'withdateranges' is TRUE
        let html = """
        <html>
        <body style='margin:0;background:#000;'>
            <div id='tv' style='height:100vh;'></div>
            <script src='https://s3.tradingview.com/tv.js'></script>
            <script>
            new TradingView.widget({
                "autosize": true,
                "symbol": "OANDA:XAUUSD",
                "interval": "\(interval)",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "save_image": false,
                "container_id": "tv"
            });
            </script>
        </body>
        </html>
        """
        uiView.loadHTMLString(html, baseURL: URL(string: "https://www.tradingview.com"))
    }
}

// MARK: - PREVIEW
struct EducationalDashboardView_Previews: PreviewProvider {
    static var previews: some View {
        EducationalDashboardView()
    }
}
