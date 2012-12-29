import theano
import theano.tensor as T
import numpy as np

obs_mat = T.dmatrix("observations")
state_mat = T.dmatrix("state")

multi_obs = T.dtensor3("multi_obs")
multi_state = T.dtensor3("multi_state")

tn = T.dscalar("true_negative")
tp = T.dscalar("true_positive")

#sensitivity = proportion of people positive who test
#positive.
#specificity = proportion of those negative who test
#negative

def singleStateObservation(st, obs, tp, tn):
	#st is the current state
	#obs is the current observation
	#lp is the last probability
	#tp is the probability of finding
	#a true positive, i.e. p(positive) | positive_obs
	#tn is the probability of finding a 
	#true negative, p(negative) | negative_obs

	obs_type = T.switch(T.eq(obs, 1.0), tp, tn)
	obs_prob = T.log(T.switch(T.eq(st, obs), obs_type, 1.0 - obs_type))
	return obs_prob


def stateSeriesObservation(ss, obss, lp, tp, tn):
	#outputs_info = T.as_tensor_variable(np.asarray(0, tp.dtype))
	result, updates = theano.map(fn = singleStateObservation, non_sequences = [tp, tn], sequences = [ss, obss])

	return T.sum(result)



outputs_info = T.as_tensor_variable(np.asarray(0, tp.dtype))
all_series_obs, all_updates = theano.scan(fn = stateSeriesObservation, sequences = [state_mat, obs_mat], non_sequences = [tp, tn], outputs_info = outputs_info )

final_prob = all_series_obs[-1]

matObs = theano.function(inputs = [state_mat, obs_mat, tp, tn], outputs = final_prob, updates = all_updates)

if __name__ == '__main__':
	imat = np.array([[1., 0., 0.,0.], [0., 1., 1.,0.], [0.,1.,0.,1.]])
	omat = np.array([[1., 0., 0.,0.], [0., 1., 1.,0.], [0.,1.,0.,1.]])

	print(matObs(imat, omat, 1.0, 1.0))