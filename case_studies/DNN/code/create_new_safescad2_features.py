import pandas as pd
import math

def create_tot_categoriesTrain(df,params):
    target = params['target']
    rt_mean = df[target].mean()
    rt_stdev = df[target].std()
    bound_1 = rt_mean-rt_stdev
    bound_2 = rt_mean+rt_stdev
    bins = [float('-inf'),bound_1,bound_2,float('inf')]
    labels = [0,1,2]
      
    return pd.cut(df[target],bins,labels=labels)

def calc_dist(x1,x2,y1,y2):
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist

def create_new_features(df,params):
    print(df.shape)
    df = df.head(df.shape[0]//params['num_of_rows_to_cumulate']*params['num_of_rows_to_cumulate'])
    print(df.shape)
    
    df_ulti = pd.DataFrame()
    
    for ind in range(0,df.shape[0],params['num_of_rows_to_cumulate']):
        df_temp = df[ind:ind+params['num_of_rows_to_cumulate']]
        
        df_one_row = pd.DataFrame()
        df_one_row.loc[0,'number_of_eye_movements'] = df_temp.drop_duplicates(subset=['LeftPupilX', 'RightPupilX','LeftPupilY','RightPupilY']).shape[0]
        df_one_row.loc[0,'number_of_look_changes'] = df_temp.drop_duplicates(subset=['locationX','locationY']).shape[0]
        
        df_temp['speedDiff'] = df_temp['CurrentSpeed'].diff()
        df_one_row.loc[0,'number_of_speed_changes'] = df_temp[df_temp['speedDiff'] != 0].shape[0]
        
        df_temp['steerDiff'] = df_temp['CurrentSteer'].diff()
        df_one_row.loc[0,'number_of_steer_positions'] = df_temp[df_temp['steerDiff'] != 0].shape[0]
        
        df_one_row.loc[0,'percentage_of_screen_look'] = round(float(df_temp.loc[df_temp.ScreenLook==1,:].shape[0]) / float(df_temp.shape[0]) * 100,2)
        
        ####################
        drop_dupl = df_temp.copy()
        drop_dupl.reset_index(drop=True,inplace=True)
        drop_dupl['distLeft'] = 0
        drop_dupl['distRight'] = 0
        for j in range(1,drop_dupl.shape[0]):
            drop_dupl.loc[j,'distLeft'] = calc_dist(float(drop_dupl.loc[j,'LeftPupilX']),float(drop_dupl.loc[j-1,'LeftPupilX']),
                                                    float(drop_dupl.loc[j,'LeftPupilY']),float(drop_dupl.loc[j-1,'LeftPupilY']))
            drop_dupl.loc[j,'distRight'] = calc_dist(float(drop_dupl.loc[j,'RightPupilX']),float(drop_dupl.loc[j-1,'RightPupilX']),
                                                    float(drop_dupl.loc[j,'RightPupilY']),float(drop_dupl.loc[j-1,'RightPupilY']))
            
        df_one_row.loc[0,'sum_distance_of_eyes'] = drop_dupl['distLeft'].sum() + drop_dupl['distRight'].sum()
        
        ####################
        drop_dupl = df_temp.copy()
        drop_dupl.reset_index(drop=True,inplace=True)
        drop_dupl['distLook'] = 0
        for w in range(1,drop_dupl.shape[0]):
            drop_dupl.loc[w,'distLook'] = calc_dist(float(drop_dupl.loc[w,'locationX']),float(drop_dupl.loc[w-1,'locationX']),
                                                    float(drop_dupl.loc[w,'locationY']),float(drop_dupl.loc[w-1,'locationY']))
                        
        df_one_row.loc[0,'sum_distance_of_looks'] = drop_dupl['distLook'].sum() 
        
        ####################
        drop_dupl = df_temp.copy()
        drop_dupl.reset_index(drop=True,inplace=True)
        drop_dupl['distSteer'] = 0
        for k in range(1,drop_dupl.shape[0]):
            drop_dupl.loc[k,'distSteer'] = abs(float(drop_dupl.loc[k,'CurrentSteer']) - float(drop_dupl.loc[k-1,'CurrentSteer']))
            
        df_one_row.loc[0,'sum_distance_of_steer'] = drop_dupl['distSteer'].sum()
        
        ####################
        df_one_row.loc[0,'average_speed'] = df_temp['CurrentSpeed'].mean()
        df_one_row.loc[0,'average_GSR_Resistance'] = df_temp['GSR Resistance'].mean()
        df_one_row.loc[0,'average_GSR_Conductance'] = df_temp['GSR Conductance'].mean()
        df_one_row.loc[0,'average_CurrentBrake'] = df_temp['CurrentBrake'].mean()
              
        ####################
        
        df_ulti = df_ulti.append(df_one_row, ignore_index=True)
    
    
    df_ulti['difference_of_average_speed_from_previous_data'] = df_ulti['average_speed'].diff().fillna(0)
    df_ulti['difference_of_average_GSR_Resistance_from_previous_data'] = df_ulti['average_GSR_Resistance'].diff().fillna(0)
    df_ulti['difference_of_average_GSR_Conductance_from_previous_data'] = df_ulti['average_GSR_Conductance'].diff().fillna(0)
    df_ulti['difference_of_average_CurrentBrake_from_previous_data'] = df_ulti['average_CurrentBrake'].diff().fillna(0)
    
    print(df_ulti.shape)
    print('-----')
    return df_ulti

################################################################################################
params = {
            'num_of_rows_to_cumulate' : 10, #10 or 100 or 500
            'target':'reaction_time',
            'used_cols_init':['Collision','Crosstype',
                         'CurrentBrake','CurrentSpeed','CurrentSteer',
                         'FalseAlarm', 'LeftPupilX', 'LeftPupilY',
                         'locationX','locationY', 'RightPupilX',
                         'RightPupilY', 'ScreenLook',
                         'Warnings', 'GSR Resistance', 'GSR Conductance','respondent',
                         'PPG', 'reaction_time'],
            'file_path':'dataset/warn2AlarmOn.csv',
            
            }

# load the data
df = pd.read_csv(params['file_path'],usecols=params['used_cols_init'])
# create sampleID - it is needed to separate the data
df['sampleID'] = df.apply(lambda x: str(x['respondent']) + str(x['reaction_time']),axis=1)
df[params['target']] = create_tot_categoriesTrain(df,params)
df = df.drop(columns=['respondent'])

# create cumulated features
df_new = df.groupby('sampleID').apply(lambda x: create_new_features(x,params))
df_new.reset_index(inplace=True)
# filter the duplicated data
id_and_target = df.drop_duplicates(subset=['sampleID'])[['sampleID',params['target']]].reset_index(drop=True)
df_new = pd.merge(df_new, id_and_target, how='left')
# save the new file
df_new.to_csv('dataset/new_features_cumulated_'+str(params['num_of_rows_to_cumulate'])+'NEW.csv',index=False)

