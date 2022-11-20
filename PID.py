'''
@Copyright (C): 2010-2019, Shenzhen Yahboom Tech
@Author: Malloy.Yuan
@Date: 2019-07-30 20:34:09
@LastEditors: Malloy.Yuan
@LastEditTime: 2019-08-08 16:10:46
'''

#*****************************************************************#
#                       Incremental PID system                    #            
#*****************************************************************#
class IncrementalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
 
        self.PIDOutput = 0.0             
        self.SystemOutput = 0.0         
        self.LastSystemOutput = 0.0    
 
        self.Error = 0.0              
        self.LastError = 0.0
        self.LastLastError = 0.0
 

    def SetStepSignal(self,StepSignal):
        self.Error = StepSignal - self.SystemOutput
        IncrementValue = self.Kp * (self.Error - self.LastError) +\
        self.Ki * self.Error +\
        self.Kd * (self.Error - 2 * self.LastError + self.LastLastError)

        self.PIDOutput += IncrementValue
        self.LastLastError = self.LastError
        self.LastError = self.Error


    def SetInertiaTime(self,InertiaTime,SampleTime):
        self.SystemOutput = (InertiaTime * self.LastSystemOutput + \
            SampleTime * self.PIDOutput) / (SampleTime + InertiaTime)

        self.LastSystemOutput = self.SystemOutput
 
 
# *****************************************************************#
#                      Positional PID system                      #
# *****************************************************************#
class PositionalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
 
        self.SystemOutput = 0.0
        self.ResultValueBack = 0.0
        self.PidOutput = 0.0
        self.PIDErrADD = 0.0
        self.ErrBack = 0.0
    

    def SetStepSignal(self,StepSignal):
        Err = StepSignal - self.SystemOutput
        KpWork = self.Kp * Err
        KiWork = self.Ki * self.PIDErrADD
        KdWork = self.Kd * (Err - self.ErrBack)
        self.PidOutput = KpWork + KiWork + KdWork
        self.PIDErrADD += Err
        if self.PIDErrADD > 2000:
            self.PIDErrADD = 2000
        if self.PIDErrADD < -2500:
            self.PIDErrADD = -2500
        self.ErrBack = Err
        

    def SetInertiaTime(self, InertiaTime,SampleTime):
           self.SystemOutput = (InertiaTime * self.ResultValueBack + \
           SampleTime * self.PidOutput) / (SampleTime + InertiaTime)

           self.ResultValueBack = self.SystemOutput
       