cd ..
base_str="
python run.py --agt 9 --usr 1 --max_turn 20 \
 	      --movie_kb_path ./deep_dialog/data/movie_kb.1k.p \
          --goal_file_path ./deep_dialog/data/user_goals_first_turn_template.part.movie.v1.p \
 	      --dqn_hidden_size 80 \
 	      --experience_replay_pool_size 1000 \
 	      --simulation_epoch_size 100 \
 	      --act_level 0 \
 	      --slot_err_prob 0.00 \
 	      --intent_err_prob 0.00 \
 	      --batch_size 16 \
 	      --warm_start 1 \
 	      --warm_start_epochs 120  "

# secondary_str="--run_mode 3 \
#           --episodes 500 \
#           --write_model_dir ./deep_dialog/checkpoints/rl_agent/test/ \
#           --trained_model_path ./deep_dialog/checkpoints/rl_agent/control/agt_9_76_170_0.93000.p \ "

read secondary_str

#Combining strings
new_str="$base_str $secondary_str"

# echo $new_str
eval $new_str
