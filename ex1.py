import pygame
from pygame.locals import *
import numpy as n
import pygame.gfxdraw as pydraw

#
# A simple demonstration of incoherent scatter from ionospheric plasma
# (c) 2017 Juha Vierinen
#

class plasma:
    
    def __init__(self,n_part=100,vel=10.0, dt=0.05, dx=1.0):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 800, 640
        self.n_part=n_part
        n.random.seed(1)        
        self.posx=n.random.rand(n_part)*self.width*dx
        self.posy=n.random.rand(n_part)*self.height*dx

        self.velx=n.random.randn(n_part)*vel
        self.vely=n.random.randn(n_part)*vel
        self.k=1.0/5.0
        self.radar_vol=(400,320,800,640)
        self.radar_loc=n.array([-100e3,-100e3])
        self.voltage=n.zeros(self.width,dtype=n.complex64)
        self.voltage_idx=0
        self.t=0.0
        self.dt=dt
        self.dx=dx

        
    def on_init(self):
        pygame.init()

#        print(pygame.font.get_fonts())
        self.font=pygame.font.Font("./cmunrm.ttf",26)
        self.fonte=pygame.font.Font("./cmunrm.ttf",2)
        self.eltxt = self.font.render("+", True, (255, 255, 255))
        
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF, 32)
        self.s = pygame.Surface((self.size),pygame.SRCALPHA)  # the size of your rect
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    # calculate new positions,
    # calculate scattered voltage
    def on_loop(self):
        
        self.posx=self.posx+self.velx*self.dt#,self.width*self.dx)
        self.posy=self.posy+self.vely*self.dt#,self.height*self.dx)

        self.t+=self.dt
        self.voltage_idx=(self.voltage_idx+1)%self.width
        self.voltage[self.voltage_idx]=0.0
        for i in range(self.n_part):
            
            self.voltage[self.voltage_idx]+=1.0/n.sqrt(self.n_part)*n.exp(1j*self.k*n.sqrt(((self.posx[i]-self.radar_loc[0])**2.0+(self.posy[i]-self.radar_loc[1])**2.0)))

    def on_render(self):
        incol=(255,255,255)
        outcol=(55,55,55)
        self._display_surf.fill((0,0,0))
        for i in range(self.n_part):
            col=incol
            pos=(int(n.mod(self.posx[i]/self.dx,self.width)),int(n.mod(self.posy[i]/self.dx,self.height)))
            pydraw.aacircle(self._display_surf, pos[0], pos[1], 5, col)
#            self._display_surf.blit(self.eltxt,(pos[0]-5,pos[1]-5))
            

        # draw voltage
        # first create a black background for points
        #for i in range(self.width-300):
         #   idx=(self.voltage_idx-i)%self.width
          #  pygame.draw.circle(self._display_surf,(0,0,0), (i+300,int(500+30*self.voltage[idx].real)), 10)
           # pygame.draw.circle(self._display_surf,(0,0,0), (i+300,int(500+30*self.voltage[idx].imag)), 10)
            
        for i in range(450):
            idx=(self.voltage_idx-i)%self.width            
            pygame.draw.circle(self._display_surf,(150,150,255), (i+300,int(500+30*self.voltage[idx].real)), 1)
            pygame.draw.circle(self._display_surf,(255,150,150), (i+300,int(500+30*self.voltage[idx].imag)), 1)

        

        # draw complex voltage in Re-Im plane
        for i in range(self.width-100):
            idx=(self.voltage_idx-i)%self.width
            pygame.draw.circle(self._display_surf,(255,255,0), (100+int(30*self.voltage[idx].real),500+int(30*self.voltage[idx].imag)), 2)

        # draw axis
        pygame.draw.aaline(self._display_surf,(255,255,255),(100,620),(100,380))
        pygame.draw.aaline(self._display_surf,(255,255,255),(100,380),(110,400))
        pygame.draw.aaline(self._display_surf,(255,255,255),(100,380),(90,400))
        
        pygame.draw.aaline(self._display_surf,(255,255,255),(0,500),(220,500))
        pygame.draw.aaline(self._display_surf,(255,255,255),(220,500),(200,510))
        pygame.draw.aaline(self._display_surf,(255,255,255),(220,500),(200,490))
            
        retext = self.font.render("Re", True, (255, 255, 255))
        self._display_surf.blit(retext,(220,500))
        imtext = self.font.render("Im", True, (255, 255, 255))
        self._display_surf.blit(imtext,(120,380))

        pygame.draw.aaline(self._display_surf,(255,255,255),(300,500),(780,500))
        pygame.draw.aaline(self._display_surf,(255,255,255),(780,500),(760,490))
        pygame.draw.aaline(self._display_surf,(255,255,255),(780,500),(760,510))

        pygame.draw.aaline(self._display_surf,(255,255,255),(300,620),(300,380))
        pygame.draw.aaline(self._display_surf,(255,255,255),(300,380),(290,400))
        pygame.draw.aaline(self._display_surf,(255,255,255),(300,380),(310,400))

        ttext = self.font.render("t", True, (255, 255, 255))
        self._display_surf.blit(ttext,(760,510))
        
        vttext = self.font.render("V(t)", True, (255, 255, 255))
        self._display_surf.blit(vttext,(320,380))
        
        
        pygame.display.flip()
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    p = plasma()
    p.on_execute()
