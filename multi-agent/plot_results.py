import numpy as np
import os.path
import matplotlib.pyplot as plt

def main():

	single_setting_line_plot(var_value=0.2)
	var_effect_line_plot()

	var_effect_line_plot(changevar='alphas',var_values=[0.1, 0.2, 0.3, 0.4, 0.5])
	var_effect_line_plot(changevar='alphas',var_values=[0.1, 0.2, 0.3, 0.4, 0.5],plotWinners=True)

	var_effect_line_plot(changevar='gammas',var_values=[0.1, 0.5, 0.7, 0.9])
	var_effect_line_plot(changevar='gammas',var_values=[0.1, 0.5, 0.7, 0.9],plotWinners=True)

	var_effect_line_plot(changevar='init_values',greekVar=False,var_values=[0, 5, 15, 50])
	var_effect_line_plot(changevar='init_values',greekVar=False,var_values=[0, 5, 15, 50],plotWinners=True)

	var_effect_line_plot(changevar='init_values',greekVar=False,var_values=[0, 5, 15, 50])
	var_effect_line_plot(changevar='init_values',greekVar=False,var_values=[0, 5, 15, 50],plotWinners=True)

	var_effect_line_plot(changevar='selection_func',greekVar=False,var_values=['epsilon_greedy({0})'.format(e) for e in  [0,0.1,0.5,0.9]])
	var_effect_line_plot(changevar='selection_func',greekVar=False,var_values=['epsilon_greedy({0})'.format(e) for e in  [0,0.1,0.5,0.9]],plotWinners=True)
	


	var_effect_line_plot()		

def load_results(algorithm,num_pred,changevar,var_value):
	"""
	returns winners_mat and steps_mat for given settings
	returns false, false as arrays if no such file exists (for consistency)
	"""

	filebase = "data/{0}.p={1},{2}={3}".format(algorithm,num_pred,changevar,var_value)
	if os.path.isfile(filebase+ '.winners.csv') and  os.path.isfile(filebase+ '.steps.csv'):
		
		winners_mat = np.genfromtxt(filebase+ '.winners.csv',skiprows=0)
		steps_mat = np.genfromtxt(filebase+ '.steps.csv',skiprows=0)

		return winners_mat, steps_mat
	else:
		return np.array(False), np.array(False)



def single_setting_line_plot(algorithm="Q",num_pred =2,changevar="alpha",var_value=0.1):
	"""
	Plot episodes on x axis, steps on y axis and winners on y axis if num_preds > 1
	for a single algorithm/settings
	"""

	winners_mat, steps_mat = load_results(algorithm,num_pred,changevar,var_value)

	if winners_mat.any():

		steps  =  np.average(steps_mat,axis=0)
		winners = np.average(winners_mat,axis=0)

		fig, ax1 = plt.subplots()
		ax1.plot(steps,'b')
		ax1.set_xlabel('Episode')
		ax1.set_ylabel('Number of steps untill game ends',color='b')
		for tl in ax1.get_yticklabels():
			tl.set_color('b')
		ax1.yaxis.grid()
		ax1.xaxis.grid()
		ax2 = ax1.twinx()
		ax2.plot(winners,'r')
		ax2.set_ylabel('Proportion of games won by the predators',color='r')
		for tl in ax2.get_yticklabels():
			tl.set_color('r')
		plt.show()

def var_effect_line_plot(algorithm="Q",num_pred =2,changevar="alpha",var_values=[0.1, 0.2, 0.3, 0.4],plotWinners=False,greekVar=True):
	"""
	Plots the episode on the x axis
	On the y axis: Steps if plotWinners = False, else proportion won by preds
	Plots different colored lines for changevar and values provided
	"""

	plt.hold(True)
	plt.grid(b=True, which='both', color='0.65',linestyle='-')

	for var_value in var_values:

		winners_mat, steps_mat = load_results(algorithm,num_pred,changevar,var_value)

		if plotWinners:
			mat = winners_mat
			plt.ylabel('Proportion of games won by the predators')
		else:
			mat = steps_mat
			plt.ylabel('Number of steps untill game ends')

		if mat.any():

			yvar = np.average(mat,axis=0)

			xs = range(len(yvar))
			if greekVar:
				plt.plot(xs, yvar, label=r'$\{0}: {1}$'.format(changevar, var_value))
			else:
				plt.plot(xs, yvar, label='${0}: {1}$'.format(changevar, var_value))


	plt.legend()
	plt.xlabel('Episode')
	plt.show()


def plot_winner_scatter(steps,winners):
    """
    Plots an awesome scatterplot!
    Two lists of length of total episodes:
        winners: keeping track of who won (1 = pred, 0=prey)
        steps: numer of steps to end game
    """

    episodes = range(len(winners))
    #create tuples for prey and pred with the index of the episode on which they 
    # won and the number of steps it took
    prey_tup = [(e,s) for w,s,e in zip(winners,steps,episodes) if w ==0]
    pred_tup = [(e,s) for w,s,e in zip(winners,steps,episodes) if w ==1]

    prey_episodes = [e for e,_ in prey_tup]
    prey_steps = [-s for _,s in prey_tup]

    pred_episodes = [e for e,_ in pred_tup]
    pred_steps = [s for _,s in pred_tup]

    #plot the steps/episodes line
    plt.scatter(prey_episodes,prey_steps,color='red',s=1)
    plt.scatter(pred_episodes,pred_steps,color='blue',s=1)
    plt.grid()
    plt.yticks(plt.yticks()[0], [abs(y) for y in plt.yticks()[0]] )
    plt.ylabel('< Steps untill prey wins                  Steps untill predator wins >')
    plt.xlabel('Episodes')
    plt.xlim([0, len(episodes)])


if __name__ == '__main__':
    	main()
