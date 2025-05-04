import json
import random

def generate_first_order_system_dataset(num_samples):
    dataset = []
    
    for i in range(num_samples):
        A = random.uniform(0.1, 20)
        B = random.uniform(0.1, 20)
        # A/(s+B)
        cT = 3/B
        
        gain_margin_min = random.uniform(5, 10)
        phase_margin_min = random.uniform(45, 90)
        settling_time_min_fast = random.uniform(0, 0.001 * cT)
        settling_time_max_fast = random.uniform(0.3* cT, 0.5 * cT)
        settling_time_min_moderate = random.uniform(0.1*cT, 0.5*cT)
        settling_time_max_moderate = random.uniform(cT, 5*cT)
        settling_time_min_slow = random.uniform(5 * cT, 10 * cT)
        settling_time_max_slow = random.uniform(20 * cT, 30 * cT)
        overshoot_max = random.uniform(5, 20)
        steadystate_error_max = 0.0001
        metadata = "First order system with different response speed requirements."
        
        system_data = {
            "id": i,
            "num": [A],
            "den": [1, B],
            "gain_margin_min": gain_margin_min,
            "phase_margin_min": phase_margin_min,
            "settling_time_min_fast": settling_time_min_fast,
            "settling_time_max_fast": settling_time_max_fast,
            "settling_time_min_moderate": settling_time_min_moderate,
            "settling_time_max_moderate": settling_time_max_moderate,
            "settling_time_min_slow": settling_time_min_slow,
            "settling_time_max_slow": settling_time_max_slow,
            "overshoot_max": overshoot_max,
            "steadystate_error_max": steadystate_error_max,
            "metadata": metadata
        }
        
        dataset.append(system_data)
    
    return dataset



def generate_second_order_system_dataset(num_samples):
    dataset = []
    
    for i in range(num_samples):
        zeta = random.uniform(0.1, 0.99)
        omega = random.uniform(0.1, 5)
        A = random.uniform(0.1,20)

        sT = 4/(omega*zeta)
        
        gain_margin_min = random.uniform(5, 10)
        phase_margin_min = random.uniform(45, 65)
        settling_time_min_fast = random.uniform(0, 0.05 * sT)
        settling_time_max_fast = random.uniform(sT, 1.5 * sT)
        settling_time_min_moderate = random.uniform(2 * sT, 2.5 * sT)
        settling_time_max_moderate = random.uniform(3 * sT, 4 * sT)
        settling_time_min_slow = random.uniform(4 * sT, 5 * sT)
        settling_time_max_slow = random.uniform(6 * sT, 10 * sT)
        overshoot_max = random.uniform(5, 20)
        steadystate_error_max = 0.0001
        metadata = "Second order system with different response speed requirements."
        
        system_data = {
            "id": i,
            "num": [A],
            "den": [1, 2*zeta*omega, omega*omega],
            "gain_margin_min": gain_margin_min,
            "phase_margin_min": phase_margin_min,
            "settling_time_min_fast": settling_time_min_fast,
            "settling_time_max_fast": settling_time_max_fast,
            "settling_time_min_moderate": settling_time_min_moderate,
            "settling_time_max_moderate": settling_time_max_moderate,
            "settling_time_min_slow": settling_time_min_slow,
            "settling_time_max_slow": settling_time_max_slow,
            "overshoot_max": overshoot_max,
            "steadystate_error_max": steadystate_error_max,
            "metadata": metadata
        }
        
        dataset.append(system_data)
    
    return dataset


# sec_dataset = generate_second_order_system_dataset(num_samples)


def generate_first_order_system_w_delay_dataset(num_samples):
    dataset = []
    for i in range(num_samples):
        A = round(random.uniform(0.1, 20), 3)
        B = round(random.uniform(0.1, 20), 3)
        # A/(s+B)
        cT = round(3/B, 2)
        tau_min = round(0.1 * cT, 3)
        tau_max = round(0.2 * cT, 3)
        tau = round(random.uniform(tau_min, tau_max), 3)
        
        # consider smaller delay (upper bound for tau )
        # settling time should related to delay (4*tau ~ 10*tau) 
        # wl < 4/(4*tau)
        # Ts ~= 3/wL

        gain_margin_min = round(random.uniform(5, 10), 3)
        phase_margin_min = round(random.uniform(10, 45), 3)
        settling_time_max = round(random.uniform(40 * tau, 50 * tau), 3)
        settling_time_min = round(random.uniform(4 * tau, 5 * tau), 3)
        overshoot_max = round(random.uniform(5, 20), 3)
        steadystate_error_max = 0.01
        metadata = "First order system with delay."

    
        
        system_data = {
            "id": i,
            "num": [A],
            "den": [1, B],
            "tau": tau,
            "gain_margin_min": gain_margin_min,
            "phase_margin_min": phase_margin_min,
            "settling_time_min": settling_time_min,
            "settling_time_max": settling_time_max,
            "overshoot_max": overshoot_max,
            "steadystate_error_max": steadystate_error_max,
            "metadata": metadata
        }
        
        dataset.append(system_data)
    
    return dataset


def generate_unstable_first_order_system_dataset(num_samples):
    dataset = []
    
    for i in range(num_samples):
        A = random.uniform(0.1, 20)
        # B = random.uniform(0.1, 20) # Stable system
        B = random.uniform(0, -20) # Unstable system
        # A/(s+B)
        cT = 3/abs(B)
        
        gain_margin_min = random.uniform(5, 10)
        phase_margin_min = random.uniform(45, 90)
        settling_time_min = random.uniform(0, 0.001 * cT)
        settling_time_max = random.uniform(0.3* cT, 0.5 * cT)
        overshoot_max = random.uniform(5, 20)
        steadystate_error_max = 0.0001
        metadata = "First order system with different response speed requirements."
        
        system_data = {
            "id": i,
            "num": [A ],
            "den": [1, B],
            "gain_margin_min": gain_margin_min,
            "phase_margin_min": phase_margin_min,
            "settling_time_min": settling_time_min,
            "settling_time_max": settling_time_max,
            "overshoot_max": overshoot_max,
            "steadystate_error_max": steadystate_error_max,
            "metadata": metadata
        }
        
        dataset.append(system_data)
    
    return dataset


def generate_unstable_second_order_system_dataset(num_samples):
    dataset = []
    
    for i in range(num_samples):
        if i %2 == 0:

            zeta = random.uniform(0.1, 0.99)
            omega = random.uniform(0.1, 5)
            A = random.uniform(0.1,20)

            sT = 4/(omega*zeta)
            
            gain_margin_min = random.uniform(5, 10)
            phase_margin_min = random.uniform(45, 65)
            settling_time_min_fast = random.uniform(0, 0.05 * sT)
            settling_time_max_fast = random.uniform(sT, 1.5 * sT)
            settling_time_min_moderate = random.uniform(2 * sT, 2.5 * sT)
            settling_time_max_moderate = random.uniform(3 * sT, 4 * sT)
            settling_time_min_slow = random.uniform(4 * sT, 5 * sT)
            settling_time_max_slow = random.uniform(6 * sT, 10 * sT)
            overshoot_max = random.uniform(5, 20)
            steadystate_error_max = 0.0001
            metadata = "Second order system with different response speed requirements."
            
            system_data = {
                "id": i,
                "num": [A],
                "den": [1, -2*zeta*omega, omega*omega],
                "gain_margin_min": gain_margin_min,
                "phase_margin_min": phase_margin_min,
                "settling_time_min_fast": settling_time_min_fast,
                "settling_time_max_fast": settling_time_max_fast,
                "settling_time_min_moderate": settling_time_min_moderate,
                "settling_time_max_moderate": settling_time_max_moderate,
                "settling_time_min_slow": settling_time_min_slow,
                "settling_time_max_slow": settling_time_max_slow,
                "overshoot_max": overshoot_max,
                "steadystate_error_max": steadystate_error_max,
                "metadata": metadata
            }

        else:

            A = random.uniform(0.1,20)
            B = random.uniform(0.1, 20)
            C = random.uniform(0,-20)
            # A/((s+B)(S+C))
            sT = 3/min(B,abs(C))
            
            gain_margin_min = random.uniform(5, 10)
            phase_margin_min = random.uniform(45, 65)
            settling_time_min_fast = random.uniform(0, 0.05 * sT)
            settling_time_max_fast = random.uniform(sT, 1.5 * sT)
            settling_time_min_moderate = random.uniform(2 * sT, 2.5 * sT)
            settling_time_max_moderate = random.uniform(3 * sT, 4 * sT)
            settling_time_min_slow = random.uniform(4 * sT, 5 * sT)
            settling_time_max_slow = random.uniform(6 * sT, 10 * sT)
            overshoot_max = random.uniform(5, 20)
            steadystate_error_max = 0.0001
            metadata = "Second order system with different response speed requirements."
            
            system_data = {
                "id": i,
                "num": [A],
                "den": [1, B+C, B*C],
                "gain_margin_min": gain_margin_min,
                "phase_margin_min": phase_margin_min,
                "settling_time_min_fast": settling_time_min_fast,
                "settling_time_max_fast": settling_time_max_fast,
                "settling_time_min_moderate": settling_time_min_moderate,
                "settling_time_max_moderate": settling_time_max_moderate,
                "settling_time_min_slow": settling_time_min_slow,
                "settling_time_max_slow": settling_time_max_slow,
                "overshoot_max": overshoot_max,
                "steadystate_error_max": steadystate_error_max,
                "metadata": metadata
            }
        
        dataset.append(system_data)
    
    return dataset



def generate_unstable_higher_order_system_dataset(num_samples):
    dataset = []
    
    for i in range(num_samples):
        if i // 10 < 1:


            A = random.uniform(0.1, 20)
            B = random.uniform(0, -20)
            zeta = random.uniform(0.3, 0.99)
            omega = random.uniform(200, 300)
            cT = 3/abs(B)
            
            gain_margin_min = random.uniform(5, 10)
            phase_margin_min = random.uniform(45, 90)
            settling_time_min = random.uniform(0.1*cT, 0.5*cT)
            settling_time_max = random.uniform(1.5*cT, 3*cT)
            overshoot_max = random.uniform(5, 20)
            steadystate_error_max = 0.0001
            metadata = "Third order system with different response speed requirements."
            
            system_data = {
                "id": i,
                "num": [A],
                "den": [1, 2*zeta*omega +B, omega**2+2*zeta*omega*B, B*omega**2],
                "gain_margin_min": gain_margin_min,
                "phase_margin_min": phase_margin_min,
                "settling_time_min": settling_time_min,
                "settling_time_max": settling_time_max,
                "overshoot_max": overshoot_max,
                "steadystate_error_max": steadystate_error_max,
                "metadata": metadata
            }



        elif i // 10 < 2:

            A = random.uniform(0.1,20)
            zeta = random.uniform(0.1, 0.99)
            omega = random.uniform(0.1, 5)
            B = random.uniform(100,200)
            sT = 4/(omega*zeta)
            
            gain_margin_min = random.uniform(5, 10)
            phase_margin_min = random.uniform(45, 60)
            settling_time_min = random.uniform(sT, 2 * sT)
            settling_time_max = random.uniform(3 * sT, 4 * sT)
            overshoot_max = random.uniform(5, 20)
            steadystate_error_max = 0.0001
            metadata = "Third order system with different response speed requirements."
            
            system_data = {
                "id": i,
                "num": [A],
                "den": [1, -2*zeta*omega +B, omega**2-2*zeta*omega*B, B*omega**2],
                "gain_margin_min": gain_margin_min,
                "phase_margin_min": phase_margin_min,
                "settling_time_min": settling_time_min,
                "settling_time_max": settling_time_max,
                "overshoot_max": overshoot_max,
                "steadystate_error_max": steadystate_error_max,
                "metadata": metadata
            }
            
        else:
            A = random.uniform(2200,2800)
            B = random.uniform(15,20)
            zeta = random.uniform(0.001,0.01)
            omega = random.uniform(20,25)
            sT = random.uniform(1,4)
            
            gain_margin_min = random.uniform(5, 10)
            phase_margin_min = random.uniform(45, 50)
            settling_time_min = random.uniform(sT, 1.5 * sT)
            settling_time_max = random.uniform(5 * sT, 7 * sT)
            overshoot_max = random.uniform(5, 20)
            steadystate_error_max = 0.0001
            metadata = "Fifth order system with different response speed requirements."
            
            system_data = {
                "id": i,
                "num": [A],
                "den": [1, 2*zeta*omega +B, omega**2+2*zeta*omega*B, B*omega**2,0,0],
                "gain_margin_min": gain_margin_min,
                "phase_margin_min": phase_margin_min,
                "settling_time_min": settling_time_min,
                "settling_time_max": settling_time_max,
                "overshoot_max": overshoot_max,
                "steadystate_error_max": steadystate_error_max,
                "metadata": metadata
            }


        
        dataset.append(system_data)
    
    return dataset


# Generate dataset
num_samples = 50  # You can adjust the number of samples
dataset = generate_first_order_system_w_delay_dataset(num_samples)
# Save dataset to JSON file
with open("/home/xingang/xingang/ControlAgent/datasets/first_order_w_delay_data.json", "w") as f:
    json.dump(dataset, f, indent=4)


# # Save dataset to JSON file
# with open("/home/xingang/xingang/ControlAgent/datasets/second_order_data.json", "w") as f:
#     json.dump(sec_dataset, f, indent=4)
