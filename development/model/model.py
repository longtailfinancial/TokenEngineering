"""
The Longtail Financial Business Model. 
"""

from cryptoHypeCycle import CryptoHypeCycle

genesis_states = {
    'talent_pool': 10, # Number of prospective Token Engineers being tracked
    'training_camp': 0, # Number of prospective Token Engineers enrolled in LTF training camp
    'ltfte': 5, # Number of active LTF Token Engineers
    'senior_ltfte': 1, # Number of active senior LTF Token Engineers
    'ltfte_journal': 1, # Number of LTF Token Engineering Journal Articles written
    'ltfte_curriculum': 0, # Represents the completion of the LTF Token Engineering Curriculum
    'ltf_marketing_force': 3, # Number of Marketing resources working for LTF
    'ltf_operational_force':3, # Number of operational and sales resources working for LTF
    'ltf_brand_strength': 282, # Number of Twitter Followers
    'crypto_hype_cycle': 0.1, # Current state of the crypto hype cycle from 0-1
    'client_pool': 5, # Number of leads in the client lead pipeline
    'active_clients': 5, # Number of currently engaged, contracted clients
    'ltf_treasury': 10000, # Current funds in the LTF treasury
    'ltf_token_model_completion': 10000, # Resources invested into an LTF Token Model. When investment hits a threshold, the token is launched. 
    'client_token_treasury': 0, # Resources invested into an LTF Token Model. When investment hits a threshold, the token is launched. 
    'base_wage': 2000, # Resources invested into an LTF Token Model. When investment hits a threshold, the token is launched. 
}


params = {
    'ltf_client_token_share': 0.01, # Percentage of tokens required from clients.
    'constant_retainer_rate': 10000, # USD constant retainer charged to clients.
    'average_project_duration': 4, # Average number of months that a client is retained.
    'cost_ltf_token_model': 250000, # Average number of months that a client is retained.
    'revenue_ltf_token_model': 5000000, # Average number of months that a client is retained.
    'token_liquidation_rate': 0.1, # The percent of tokens in the token treasury that are liquidated into revenue per month.
    'token_compound_rate': 0.01, # The percent of tokens in the token treasury that are liquidated into revenue per month.
    'expansion_rate': 0.01, # Percent of talent pool to hire into marketing and operations when expanding.
    'crypto_hype_cycle_model': CryptoHypeCycle(variance=0.075), # Current state of the crypto hype cycle from 0-1
}

def crypto_hype_progression(params, step, sH, s):
    # Brownian progression
    crypto_hype_cycle_model = params['Crypto_hype_cycle_model']
    crypto_hype_cycle_model.brownian_step()
    crypto_hype = crypto_hype_cycle_model.y(crypto_hype_cycle_model.current_x)
    return ({'crypto_hype_cycle':crypto_hype})


def talent_inbound_process(params, step, sH, s):
    # Talent Pool += Number of twitter followers * crypto hype cycle * 0.1
    # Churn 10%
    ltf_twitter_followers = s['ltf_brand_strength'] # Number of Twitter Followers
    crypto_hype = s['crypto_hype_cycle'] # Current hype
    talent_pool = s['talent_pool'] # Talent Pool
    talent_pool += ltf_twitter_followers * crypto_hype * 0.1
    # Churn
    return ({'talent_pool':talent_pool})

def training_camp_enrollment_process(params, step, sH, s):
    # Talent pool * LTFTE curriculum * 0.1
    # Maximum capacity of LTFTE + 2*SeniorLTFTE
    # Churn 10%
    training_camp = s['training_camp'] # Training Camp
    talent_pool = s['talent_pool'] # Talent Pool
    ltfte_curriculum = s['ltfte_curriculum'] # LTFTE Curriculum
    training_camp_delta = talent_pool * ltfte_curriculum * 0.1
    # Max capacity
    ltfte = s['ltfte'] # LTF TE
    senior_ltfte = s['senior_ltfte'] # LTFTE Curriculum
    max_capacity = ltfte + 2 * senior_ltfte
    training_camp_delta = min(max_capacity - training_camp, training_camp_delta)
    # Churn
    return ({'training_camp_delta':training_camp_delta})

def ltfte_onboarding_process(params, step, sH, s):
    # Number of training camp recruits * LTFTE curriculum * 0.25
    # Maximum 10
    # Churn 2%
    ltfte = s['ltfte'] # LTFTE 
    training_camp = s['training_camp'] # Training Camp
    ltfte_curriculum = s['ltfte_curriculum'] # LTFTE Curriculum
    ltfte_delta = training_camp * ltfte_curriculum * 0.25
    # Max capacity
    ltfte_delta = min(10-ltfte, ltfte_delta)
    # Churn
    return ({'ltfte_delta':ltfte_delta})

def ltfte_graduation_process(params, step, sH, s):
    # Delta LTFTE one year in the past
    # Simple computation: LTFTE / 12
    # Maximum 10
    # Churn 2%
    ltfte = s['ltfte'] # LTFTE Curriculum
    senior_ltfte = s['senior_ltfte'] # LTFTE Curriculum
    senior_ltfte_delta = ltfte / 12
    # Max capacity
    senior_ltfte_delta = min(10-senior_ltfte, senior_ltfte_delta)
    # Churn
    return ({'senior_ltfte_delta':senior_ltfte_delta})

def ltfte_journal(params, step, sH, s):
    # += (Training Recruits + Token Engineers + Senior Token Engineers) / 2
    training_camp = s['training_camp'] # Training Camp
    ltfte = s['ltfte'] # LTFTE Curriculum
    senior_ltfte = s['senior_ltfte'] # LTFTE Curriculum
    delta_ltf_journal = training_camp + ltfte + senior_ltfte
    return ({'delta_ltf_journal':delta_ltf_journal})


def ltfte_curriculum(params, step, sH, s):
    # = ltfte journal articles / 100
    ltfte_journal = s['ltfte_journal'] # LTFTE Curriculum
    return ({'ltfte_curriculum':ltfte_journal / 100})

def company_expansion(params, step, sH, s):
    # Expand marketing if treasury > 150000
    # Expand operations if treasury > 150000
    # If expanding marketing, marketing force += talent_pool * expansion_rate
    # If expanding operations, operational force += talent_pool * expansion_rate
    pass


def marcomms(params, step, sH, s):
    # twitter followers += ltf marketing force * ltfte journal * base wage / 6000
    ltf_marketing_force = s['ltf_marketing_force'] # Number of Marketing resources working for LTF
    ltfte_journal = s['ltfte_journal'] # Number of Journal Articles Written
    base_wage = s['base_wage'] # Current base wage
    delta_twitter_followers = ltf_marketing_force * ltfte_journal * base_wage / 6000
    return ({'delta_twitter_followers':delta_twitter_followers})

def client_inbound_process(params, step, sH, s):
    # Number of twitter followers * crypto hype cycle * 0.05
    ltf_twitter_followers = s['ltf_brand_strength'] # Number of Twitter Followers
    crypto_hype = s['crypto_hype_cycle'] # Current hype
    client_pool = s['client_pool'] # Client Pool
    client_pool += ltf_twitter_followers * crypto_hype * 0.05
    # Churn
    return ({'client_pool':client_pool})

def sales(params, step, sH, s):
    # active clients += ltf operational force * client pool * base wage / 6000 * 0.1
    # Maximum capacity of 1/2 recruits + ltfte + 2*senior_ltfte
    ltf_operational_force = s['ltf_operational_force'] # Number of operational resources working for LTF
    client_pool = s['client_pool'] # Client Pool
    base_wage = s['base_wage'] # Current base wage
    delta_active_clients = ltf_operational_force * client_pool * base_wage / 6000 * 0.1
    # Max capacity
    training_camp = s['training_camp']
    ltfte = s['ltfte']
    senior_ltfte = s['senior_ltfte']
    max_client_capacity = 0.5 * training_camp + ltfte + 2 * senior_ltfte
    return ({
        'delta_active_clients':delta_active_clients,
        'max_client_capacity': max_client_capacity,
    })

def revenue(params, step, sH, s):
    # Treasury += active clients * constant retainer rate
    active_clients = s['active_clients']
    constant_retainer_rate = params['constant_retainer_rate']
    treasury_delta = active_clients * constant_retainer_rate
    return ({'treasury_delta':treasury_delta})

def client_project_completion(params, step, sH, s):
    # Retired Clients = Delta active clients from {average_project_duration} time periods ago
    # Simple computation = Retired clients = - active clients / {average_project_duration} 
    # active clients -= Retired Clients
    # client token treasury = retired clients * client token share * random distribution $0-30million
    active_clients = s['active_clients']
    average_project_duration = params['average_project_duration']
    retired_clients = active_clients / average_project_duration

    # Token Treasury
    ltf_client_token_share = params['ltf_client_token_share']
    client_token_treasury_delta = retired_clients * ltf_client_token_share * np.random.beta(2, 8) * 30000000
    return ({
        'retired_clients':retired_clients,
        'client_token_treasury_delta': client_token_treasury_delta,
    })

def ltf_token_model_progression(params, step, sH, s):
    # If LTFTE capacity is not fully utilized on clients, then it goes into LTF Token Model development
    # The cost of the LTFTE capacity is put into the Token Model R&D Pool. When this pool meets a threshold, the token is launched.
    # The token yields a fixed revenue when launched. This revenue goes into the ltf token treasury
    pass

def token_treasury_liquidation(params, step, sH, s):
    # Liquidate tokens.
    # Treasury += liquidation rate * token treasury
    pass

def token_treasury_compound(params, step, sH, s):
    # Compound yield on treasury tokens.
    # Treasury += 1+compound rate * token treasury
    pass


