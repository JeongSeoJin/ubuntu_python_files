
import pygame
from math import *
from pygame.locals import *
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
# 화면의 범위는 가로 500, 세로 500
WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
rate = 100

# 목표 좌표
GOAL = [[300, 300], [425, 425], [75, 75]]   # 마지막 목표는 출발점


class Car:
    def __init__(self, initial_location):
        self.x, self.y = initial_location

        self.length = 15
        self.width = 10
        self.tread = 10
        self.wheel_radius = 1

        self.heading = 0

        self.speed = 0
        self.steer = 0
        self.predict_time = 0.01

        # ↓ ↓ ↓ ↓ ↓ ↓ init 에서 활용하고 싶은 인스턴스 변수가 있을 시 이곳에 작성 ↓ ↓ ↓ ↓ ↓ ↓

        # ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑

    # noinspection PyMethodMayBeStatic
    def convert_coordinate_l2g(self, d_x, d_y, d_theta):                    # local -> global 좌표 변환
        trans_matrix = np.array([[cos(d_theta), -sin(d_theta), 0],          # 변환 행렬
                                 [sin(d_theta), cos(d_theta), 0],
                                 [0, 0, 1]])
        return np.dot(trans_matrix, np.transpose([d_x, d_y, d_theta]))

    def generate_predict_pose(self):
        self.steer = min(max(self.steer, -30), 30)
        tan_dis = self.speed * self.predict_time  # 접선 이동 거리 (= 호의 길이)
        R = self.length / tan(radians(-self.steer)) if self.steer != 0 else float('inf')  # 곡률 반경
        d_theta = tan_dis / R

        predict_pose = [tan_dis, 0.0, 0.0] if R == float('inf') else [R * sin(d_theta), R * (1 - cos(d_theta)), d_theta]
        d_x, d_y, heading = np.transpose(self.convert_coordinate_l2g(predict_pose[0], predict_pose[1], d_theta + self.heading))
        return self.x + d_x, self.y + d_y, heading

    def move(self):
        self.x, self.y, self.heading = self.generate_predict_pose()

    def GUI_display(self):
        pygame.draw.circle(screen, GREEN, [GOAL[2][0], 500 - GOAL[2][1]], 10)
        pygame.draw.circle(screen, BLUE, [GOAL[0][0], 500 - GOAL[0][1]], 10)
        pygame.draw.circle(screen, BLUE, [GOAL[1][0], 500 - GOAL[1][1]], 10)

        a = atan2(self.width, self.length)
        b = sqrt(self.length ** 2 + self.width ** 2) / 2
        corner1 = [self.x + cos(self.heading - a) * b, 500 - (self.y + sin(self.heading - a) * b)]
        corner2 = [self.x + cos(self.heading + a) * b, 500 - (self.y + sin(self.heading + a) * b)]
        corner3 = [self.x + cos(self.heading + pi - a) * b, 500 - (self.y + sin(self.heading + pi - a) * b)]
        corner4 = [self.x + cos(self.heading + pi + a) * b, 500 - (self.y + sin(self.heading + pi + a) * b)]
        pygame.draw.polygon(screen, RED, [corner1, corner2, corner3, corner4])

    # set_motor_value 함수 내에서 자유롭게 작성
    def set_motor_value(self, count):
        self.speed = 30
        self.steer = 0

        # print('x: ', self.x)
        # print('y: ', self.y)
        # print('heading: ', self.heading)


def main():
    car = Car([GOAL[2][0], GOAL[2][1]])
    count = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return 0

        car.set_motor_value(count)
        car.move()

        screen.fill(WHITE)
        car.GUI_display()

        pygame.display.flip()
        clock.tick(rate)
        count += 1


if __name__ == '__main__':
    main()