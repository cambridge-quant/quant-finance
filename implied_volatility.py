import QuantLib as ql

spot_price = 188.64
risk_free_rate = 0.0525
dividend_yield = 0.0052
volatility = 0.20
days_to_maturity = 148
strike_price = 190
option_price = 11.05

alendar = ql.NullCalendar()
day_count = ql.Actual360()
today = ql.Date().todaysDate()

ql.Settings.instance().evaluationDate = today
risk_free_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(today, risk_free_rate, day_count)
)
dividend_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(today, dividend_yield, day_count)
)

spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))

expiration_date = today + ql.Period(days_to_maturity, ql.Days)
payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike_price)
exercise = ql.AmericanExercise(today, expiration_date)
american_option = ql.VanillaOption(payoff, exercise)

bsm_process = ql.BlackScholesMertonProcess(
    spot_handle, dividend_ts, risk_free_ts, volatility_handle
)

engine = ql.BinomialVanillaEngine(bsm_process, "crr", 1000)
american_option.setPricingEngine(engine)

implied_volatility = american_option.impliedVolatility(
    option_price, bsm_process, 1e-4, 1000, 1e-8, 4.0
)