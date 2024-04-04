# Optimizing-Your-Electricity-Consumption-In-Python
The title is a bit click-baity, but generally, the base software for optimization of your power consumption can be written within 10 hours, even by a non-professional. Such an example is shown here. It is still work in progress, thus nearly nothing is commented or described in detail in the code.
First we generate a zero-profile for one day on a minute basis (thus 1440 zeros). Thus, one minute os our smallest unit of time. The problem is that different power meters have different measuring intervals in Home Assistant (Shelly seems to have a dynamic interval down to a few seconds, AVM Fritz power meters are sometimes a bit dynamic but mostly they deliver 2 minute intervals. Others may be again different, IDK). 
However, we have to define a power curve for every appliance we want to include in our 'simulation'. Due to the minute interval, these curves are lists with power values (positive if we consume that power, negative if we generate it from our solar array) in one minute intervals, thus we have to flatten shorter spikes to a one-minute-average. Some power profiles are included in the code. In the future we will probably implement a file with these values to unclutter the Python file.
Our main function in this software is inject_power_value. As the name suggests, it 'injects' a power value from a device at the given 'running' (absolute) time of day. We can switch a device on by giving the inject_power_value function a 'device' that is a tiny list like coffemaker_1 = ["07:00", "09:00", coffemaker_profile_1] with a starting time and an end time plus a power profile of this device. That's all. The inject_power_value function writes and accumulates a power value to a global total_power_curve_per_day list. It's really that simple.
The shared code starts with a lot of number (the power profiles for a few devices). The main program first calculates a typical power curve of a typical sunny day in home office where we switch on the boiler for hot water early in the morning (night rather :-) ), we get up sometime at 6:30 or so and switch on the news and the coffeemaker from 07:00 to 09:00. Some devices are always-on like the refrigerator and all the IT-devices for Internet and WiFi. This day is also a laundry day, plus the dishwasher needs to be switched on too. For this day we get a simulated power curve like:

![Figure_1](https://github.com/emefff/Optimizing-Your-Electricity-Consumption-In-Python/assets/89903493/d91ecba5-133e-41a0-910e-57db982ef0b8)

As we can see, there's quite a lot going on with some spiky power values from the coffemaker, laundry machine and dishwasher (please refer to the code for details, it's all there). We find the total energy consumed to be 5.304 kWh.
The curve shown also shows negative values from the solar array. The total power consumed value does not include negative values, negative values are set to zero (in small solar arrays in EU, this energy is lost to the user!). This is very important for the optimization. Many readers will already have at least a tiny solar array (commonly referred to as 'Balkonkraftwerk' in the DACH region). So what is this little simulation even good for, if we, as solar array owners already know what to do for energy optimization ('start all appliances during solar hours' is what we need to do)? 
Of course we can investigate our usage in much greater detail and simulate (profiles needed must be available, of course!) for example, in a first step an optimum start time for the laundry machine. In the code, we just brute-force (minute by minute during a given interval of 5-16 o' clock, that's 5AM to 4PM for all Americans) and scan through a lot of energy values to find the optimum. The result after this first optimization looks like this:

![Figure_2](https://github.com/emefff/Optimizing-Your-Electricity-Consumption-In-Python/assets/89903493/4dcf5e63-048b-4764-8f9d-e107197a56a7)

We find the optimum starting time for our laundry machine to be in the interval of 520-580 minutes of this day (that is between 08:40 and 09:40 on this day). For the next round of optimization we shift the starting time of the dishwasher. The starting time of the laundry machine is set to the center value of above optimum interval, that is 09:10. We brute-force power curves again by scanning from 5-16 o'clock but with the dishwasher:

![Figure_3](https://github.com/emefff/Optimizing-Your-Electricity-Consumption-In-Python/assets/89903493/d5ff3ef4-cd53-43fa-9f84-4a52f60ae5a4)

What can we deduct from this? Optimizin the second appliance leads to overlapping with the optimized laundry machine and leads to one local maximum (the peak). It is caused by overlapping power spikes of the two devices. We want to avoid that, this directly causes the optimim interval to be much more narrow compared to the first optimization. Now we only can shift our dishwasher between 490-510 minutes, that is 08:10-08:30. If we just follow the above mentioned common rule of tiny solar array owners ('swich on all your stuff during solar hours') we could land on this local maximum if we are not careful. It would be a coincidence, though.

In the end, we can calculate the energy saved to be around 0.5kWh and simulate an optimum profile to be:

![Figure_4](https://github.com/emefff/Optimizing-Your-Electricity-Consumption-In-Python/assets/89903493/b0cb3d89-d92e-47b7-9784-d9689a11a0b2)

So what is the conclusion of all this?

1.) Even we want to optimize only two devices, time is a critcal factor. It's probably never 'perfect' when we just guess.

2.) In reality, we'd have to know our solar array and device power profiles in advance to optimize our devices in the morning! This in only possible with a good prediction of the solar power profiles and good knowledge of the device power profiles. The solar power prediction is possible in Home Assistant, but it is sometimes a bit sketchy. Today, it only works on perfect sunny days.

3.) This type of software could also be used to simulate weeks, months or years in advance. However, we'd rather need 50-100 power profiles (for example for the solar array we'd need days in summer, autumn, winter, spring with sunny, cloudy, etc. weather. Also, water boiler need less energy in summer when we also need less warm water etc. This is a lot of work.) than 5-10.

4.) If we had all the profiles needed, this could also be automated in the following way: Take a predicted solar array power profile for the current day in the morning, the user tells the system which appliances he needs on this exact day, the system performs a simulation like above in a few minutes (1-2 minutes depending on CPU power) and switches all the needed appliances on at the perfect time without user interference (except we still have to put our laundry and dishes etc. in our machines :-( ).

We think such systems are possible within the next years. They could learn the power profiles from the smart home system and perform such optimizations automatically and switch all your devices on at the perfect time during the day (appliances must have Smart Home capability). 
Smart boilers are already available, they take an electricity profile for the next day and power on accordingly. This absolutely makes sense, because water heating is one of the, if not THE, main power consumer in our households.

****** WORK IN PROGRESS PLEASE EXCUSE TYPOS ETC *****

emefff@gmx.at
