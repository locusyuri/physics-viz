clear
% 异步脉冲控制：无外部激励的复值耦合振子同步
clc
close all
rng(2026);



set(0,'defaultAxesFontName','Times New Roman');
set(0,'defaultTextFontName','Times New Roman');
set(0,'defaultAxesFontSize',12);
set(0,'defaultTextFontSize',12);
set(0,'defaultLineLineWidth',1.2);
set(0,'defaultAxesLineWidth',1.1);
set(0,'defaultFigureColor','w');

fig_dir = fullfile(pwd,'skz2_theorem4_complex_sync_GBK_figures');
if ~exist(fig_dir,'dir')
    mkdir(fig_dir);
end

%% 基本参数
Tmax = 20;
tao  = 0.10;                 %% 常值延迟 tau
step = 0.002;                % 步长

time = -tao:step:Tmax;
N    = length(time);
N1   = fix(tao/step)+1;      % 延迟步数加 1, 访问 t-tau 用 t1-N1+1
ZS   = N*2;
JD   = 13;                   %% 节点数，根据有向图修改
Dim  = 2;                    % x_m=(z_m^(1),z_m^(2))^T
YB   = 1;                    %% Monte Carlo 样本数, 画轨迹时可取 1，画均方图取50

%% 异步脉冲时刻生成: 保留 skz2 的控制设计结构
CA   = zeros(JD,1);
mczy = zeros(JD,ZS);
HSK  = zeros(JD,ZS);

for j1 = 1:JD
    CA(j1) = 2.1 + (2.2-2.1)*rand;             %% 平均脉冲率参数，\epsilon_m^2=2.2/1.2;\epsilon_m^1可取与\epsilon_m^3一样
    for z = 1:ZS
        mczy(j1,z) = 0.6 + (0.65-0.6)*rand;    %% 脉冲收缩系数μ_c1^{m}=0.65
        HSK(j1,z)  = -log(0.65^2);             %% 条件A5中μ_c1^{m}=0.65
    end
end

PJKZL = zeros(JD,1);        % 平均驻留时间
TK    = zeros(JD,ZS);       % 脉冲时刻

for j1 = 1:JD
    TK(j1,1) = 0;
    k2 = 1;
    PJKZL(j1) = HSK(j1,k2+1)/CA(j1);
    while TK(j1,k2) < Tmax && k2 < ZS-1
        TK(j1,k2+1) = TK(j1,k2) + fix((0.8+(1.2-0.8)*rand)*PJKZL(j1)/step)*step;
        k2 = k2 + 1;
        if TK(j1,k2-1) >= Tmax
            break;
        end
    end
end

PDMC  = zeros(JD,N);        % 判断是否发生脉冲
PDMCT = -ones(JD,N);        % 脉冲画图矩阵

for j1 = 1:JD
    k2 = 1;
    for t1 = 1:N
        if k2 <= ZS && abs(TK(j1,k2)-time(t1)) < 0.0001*step
            PDMC(j1,t1)  = 1;
            PDMCT(j1,t1) = 0.2*j1;
            k2 = k2 + 1;
        end
    end
end

figure('Name','Asynchronous impulsive instants');
plot(time,PDMCT,'*','MarkerSize',3);
grid on; box on;
xlabel('Time (s)');
ylabel('Node index');
title('Asynchronous impulsive instants');

%% 复值耦合振子系统参数。参数根据条件修改
% z1' = z2 - delta1*z1 + coupling + noise
% z2' = (-delta2+delta1)*z2 + (delta2*delta1-delta1^2-1)*z1
%       - r_delay*z1(t-tau) + coupling + noise

delta1  = 0.06 + 0.98i;    %% 弱阻尼复参数，使孤立系统保持非零振荡
delta2  = 0.19 + 0.32i;    %% 复值模型参数
r_delay = -0.07 + 0.22i;   %% 复值常时滞反馈系数，Y(z_m^{(1)}(t-tau))=r_delay z_m^{(1)}(t-tau) 

% 复值噪声强度
sigma1_now = 0.012 + 0.004i;%%函数g^1前面系数，同第一个程序
sigma1_tau = 0.004 + 0.002i;%%函数g^1前面系数，同第一个程序
sigma2_now = 0.011 + 0.004i;%%函数g^2前面系数，同第一个程序
sigma2_tau = 0.004 + 0.002i;%%函数g^2前面系数，同第一个程序


%% 单连边强连通有向环网络，根据有向图改
A = zeros(JD,JD);
for j1 = 1:JD-1
    A(j1,j1+1) = 1;          % 强连通有向环
end
A(JD,1) = 1;

coupling_strength = 0.035;%%整个这一块需要根据画的有向图修改
AAA = coupling_strength*A;   % 非负耦合矩阵 a_ml
Gamma = eye(Dim);            % 内耦合矩阵

%% 定理4数值条件检查量，这里仅供参考，需要自己验证
mu_max = max(mczy(:));
mu_min = min(mczy(:));

row_sum = zeros(JD,1);
for j1 = 1:JD
    row_sum(j1) = sum(AAA(j1,:))*norm(Gamma,2);
end
max_row_sum = max(row_sum);

L_now = abs(delta1) + 1 + abs(-delta2+delta1) + abs(delta2*delta1-delta1^2-1);
L_tau = abs(r_delay);
G_now = abs(sigma1_now)^2 + abs(sigma2_now)^2;
G_tau = abs(sigma1_tau)^2 + abs(sigma2_tau)^2;

mean_impulse_period = mean(PJKZL);
impulse_decay_rate  = -2*log(mu_max)/mean_impulse_period;
growth_bound        = 2*(L_now+L_tau) + 2*(G_now+G_tau) + 4*max_row_sum;
theorem4_margin     = impulse_decay_rate - growth_bound;

fprintf('\n===== Theorem 4 numerical verification =====\n');
fprintf('System: complex-valued coupled oscillator.\n');
fprintf('Synchronization: ordinary master-slave synchronization e_m=x_m-y.\n');
fprintf('Delay: constant delay tau = %.4f.\n',tao);
fprintf('delta1 = %.4f%+.4fi.\n',real(delta1),imag(delta1));
fprintf('delta2 = %.4f%+.4fi.\n',real(delta2),imag(delta2));
fprintf('r_delay = %.4f%+.4fi.\n',real(r_delay),imag(r_delay));
fprintf('Control: asynchronous impulsive control e_m(t_k^+)=mu_m^k e_m(t_k^-).\n');
fprintf('Nodes JD = %d, Monte Carlo samples YB = %d, step = %.4f.\n',JD,YB,step);
fprintf('mu_min = %.4f, mu_max = %.4f.\n',mu_min,mu_max);
fprintf('Mean impulse interval estimate = %.4f.\n',mean_impulse_period);
fprintf('Impulse decay rate estimate = %.4f.\n',impulse_decay_rate);
fprintf('System growth bound estimate = %.4f.\n',growth_bound);
fprintf('Theorem-4 numerical margin = %.4f. Positive is desirable.\n',theorem4_margin);

%% 随机数
SJ1 = randn(YB,N);            % Brownian increment dB=sqrt(step)*SJ1
SJ2 = randn(YB,N);            % 保留变量名, 与 skz2 结构一致

%% 变量初始化
ZZ = complex(zeros(YB,Dim,JD,N));    % 控制系统 x_m
ZY = complex(zeros(YB,Dim,N));       % 孤立目标系统 y
WC = complex(zeros(YB,Dim,JD,N));    % 同步误差 e_m=x_m-y

for y11 = 1:YB
    for t1 = 1:N1+1
        tt = time(t1);
        ZY(y11,1,t1) = 0.75*exp(1i*(1.10*tt+0.20)) + 0.22*cos(1.80*tt) + 0.12i*sin(1.40*tt);
        ZY(y11,2,t1) = 0.62*exp(1i*(0.95*tt-0.10)) + 0.20*sin(1.60*tt) - 0.10i*cos(1.30*tt);
        for j1 = 1:JD
            ZZ(y11,1,j1,t1) = ZY(y11,1,t1) + 0.35*cos(0.35*j1) + 0.18i*sin(0.25*j1) + 0.02*randn + 0.02i*randn;
            ZZ(y11,2,j1,t1) = ZY(y11,2,t1) + 0.30*sin(0.30*j1) - 0.16i*cos(0.20*j1) + 0.02*randn + 0.02i*randn;
            WC(y11,1,j1,t1) = ZZ(y11,1,j1,t1) - ZY(y11,1,t1);
            WC(y11,2,j1,t1) = ZZ(y11,2,j1,t1) - ZY(y11,2,t1);
        end
    end
end

%% Euler-Maruyama 主循环 + 异步脉冲控制
for y11 = 1:YB
    kk = ones(JD,1);
    for t1 = N1+1:N-1
        tt = time(t1);
        id_tau = t1 - N1 + 1;
        % 孤立目标系统 y(t)
        y_now = zeros(Dim,1);
        y_tau = zeros(Dim,1);
        y_now(1) = ZY(y11,1,t1);
        y_now(2) = ZY(y11,2,t1);
        y_tau(1) = ZY(y11,1,id_tau);
        y_tau(2) = ZY(y11,2,id_tau);

        fy = zeros(Dim,1);
        gy = zeros(Dim,1);
        fy(1) = y_now(2) - delta1*y_now(1);
        fy(2) = (-delta2+delta1)*y_now(2) + (delta2*delta1-delta1^2-1)*y_now(1) ...
              - r_delay*y_tau(1);
        gy(1) = sigma1_now*y_now(1) + sigma1_tau*y_tau(1);
        gy(2) = sigma2_now*y_now(2) + sigma2_tau*y_tau(2);

        ZY(y11,1,t1+1) = y_now(1) + step*fy(1) + gy(1)*sqrt(step)*SJ1(y11,t1);
        ZY(y11,2,t1+1) = y_now(2) + step*fy(2) + gy(2)*sqrt(step)*SJ1(y11,t1);

        for j1 = 1:JD
            x_now = zeros(Dim,1);
            x_tau = zeros(Dim,1);
            x_now(1) = ZZ(y11,1,j1,t1);
            x_now(2) = ZZ(y11,2,j1,t1);
            x_tau(1) = ZZ(y11,1,j1,id_tau);
            x_tau(2) = ZZ(y11,2,j1,id_tau);

            fx = zeros(Dim,1);
            gx = zeros(Dim,1);
            fx(1) = x_now(2) - delta1*x_now(1);
            fx(2) = (-delta2+delta1)*x_now(2) + (delta2*delta1-delta1^2-1)*x_now(1) ...
                  - r_delay*x_tau(1);
            gx(1) = sigma1_now*x_now(1) + sigma1_tau*x_tau(1);
            gx(2) = sigma2_now*x_now(2) + sigma2_tau*x_tau(2);

            coupling = zeros(Dim,1);
            for j2 = 1:JD
                if AAA(j1,j2) ~= 0
                    xj = zeros(Dim,1);
                    xj(1) = ZZ(y11,1,j2,t1);
                    xj(2) = ZZ(y11,2,j2,t1);
                    coupling = coupling + AAA(j1,j2)*(Gamma*(xj-x_now));
                end
            end

            ZZ(y11,1,j1,t1+1) = x_now(1) + step*(fx(1)+coupling(1)) + gx(1)*sqrt(step)*SJ1(y11,t1);
            ZZ(y11,2,j1,t1+1) = x_now(2) + step*(fx(2)+coupling(2)) + gx(2)*sqrt(step)*SJ1(y11,t1);

            WC(y11,1,j1,t1+1) = ZZ(y11,1,j1,t1+1) - ZY(y11,1,t1+1);
            WC(y11,2,j1,t1+1) = ZZ(y11,2,j1,t1+1) - ZY(y11,2,t1+1);

            % 异步脉冲控制: 保持 skz2 的控制设计程序
            if PDMC(j1,t1+1) > step
                ZZ(y11,1,j1,t1+1) = ZY(y11,1,t1+1) + WC(y11,1,j1,t1+1)*mczy(j1,kk(j1));
                ZZ(y11,2,j1,t1+1) = ZY(y11,2,t1+1) + WC(y11,2,j1,t1+1)*mczy(j1,kk(j1));
                WC(y11,1,j1,t1+1) = ZZ(y11,1,j1,t1+1) - ZY(y11,1,t1+1);
                WC(y11,2,j1,t1+1) = ZZ(y11,2,j1,t1+1) - ZY(y11,2,t1+1);
                kk(j1) = kk(j1) + 1;
            end
        end
    end
end

%% 后处理
ZZ1 = zeros(JD,N);
ZZ2 = zeros(JD,N);
ZY1 = zeros(N,1);
ZY2 = zeros(N,1);
WC1 = zeros(JD,N);
WC2 = zeros(JD,N);
JFWC = zeros(JD,N);

for t1 = 1:N
    ZY1(t1) = ZY(1,1,t1);
    ZY2(t1) = ZY(1,2,t1);
    for j1 = 1:JD
        ZZ1(j1,t1) = ZZ(1,1,j1,t1);
        ZZ2(j1,t1) = ZZ(1,2,j1,t1);
        WC1(j1,t1) = WC(1,1,j1,t1);
        WC2(j1,t1) = WC(1,2,j1,t1);
        JFWC(j1,t1) = sum(abs(WC(:,1,j1,t1)).^2 + abs(WC(:,2,j1,t1)).^2)/YB;
    end
end

EZ1 = zeros(JD,N);
EZ2 = zeros(JD,N);
for j1 = 1:JD
    for t1 = 1:N
        EZ1(j1,t1) = sum(abs(ZZ(:,1,j1,t1)).^2)/YB;
        EZ2(j1,t1) = sum(abs(ZZ(:,2,j1,t1)).^2)/YB;
    end
end

MSE_mean = mean(JFWC,1);
fprintf('Initial mean-square sync error = %.6e.\n',MSE_mean(N1+1));
fprintf('Final mean-square sync error   = %.6e.\n',MSE_mean(end));
fprintf('Figures exported to: %s\n\n',fig_dir);

%% 图1: 脉冲时刻
figure('Name','Asynchronous impulsive instants','Units','centimeters','Position',[3 3 12 7]);
plot(time,PDMCT,'*','MarkerSize',3);
grid on; box on;
xlabel('t');
ylabel('Node index');
title('Asynchronous impulsive instants');
print(gcf,fullfile(fig_dir,'Fig1_Impulsive_Instants.png'),'-dpng','-r600');

%% 图2: 实部同步轨迹
figure('Name','Real parts synchronization','Units','centimeters','Position',[3 3 14 8]);
plot(time,real(ZZ1),'-','LineWidth',0.9); hold on;
plot(time,real(ZZ2),'--','LineWidth',0.9);
plot(time,real(ZY1),'k-','LineWidth',2.0);
plot(time,real(ZY2),'k--','LineWidth',2.0);
grid on; box on;
xlabel('t');
ylabel('Real parts');
print(gcf,fullfile(fig_dir,'Fig2_Real_Trajectories_Sync.png'),'-dpng','-r600');

%% 图3: 虚部同步轨迹
figure('Name','Imaginary parts synchronization','Units','centimeters','Position',[3 3 14 8]);
plot(time,imag(ZZ1),'-','LineWidth',0.9); hold on;
plot(time,imag(ZZ2),'--','LineWidth',0.9);
plot(time,imag(ZY1),'k-','LineWidth',2.0);
plot(time,imag(ZY2),'k--','LineWidth',2.0);
grid on; box on;
xlabel('t');
ylabel('Imaginary parts');
print(gcf,fullfile(fig_dir,'Fig3_Imag_Trajectories_Sync.png'),'-dpng','-r600');

% %% 图4: 同步误差轨迹
% figure('Name','Synchronization errors','Units','centimeters','Position',[3 3 14 8]);
% plot(time,abs(WC1),'-','LineWidth',0.9); hold on;
% plot(time,abs(WC2),'--','LineWidth',0.9);
% grid on; box on;
% xlabel('Time (s)');
% ylabel('Synchronization error');
% print(gcf,fullfile(fig_dir,'Fig4_Synchronization_Errors.png'),'-dpng','-r600');

%% 图5: 均方同步误差
figure('Name','Mean-square synchronization errors','Units','centimeters','Position',[3 3 14 8]);
plot(time,JFWC,'LineWidth',1.0);
grid on; box on;
xlabel('Time (s)');
ylabel('Mean-square synchronization error');
print(gcf,fullfile(fig_dir,'Fig5_Mean_Square_Sync_Error.png'),'-dpng','-r600');

% %% 图6: 控制系统状态的均方轨迹
% figure('Name','Mean-square states of controlled system','Units','centimeters','Position',[3 3 14 8]);
% plot(time,EZ1,'-','LineWidth',1.0); hold on;
% plot(time,EZ2,'--','LineWidth',1.0);
% grid on; box on;
% xlabel('Time (s)');
% ylabel('Mean-square state');
% print(gcf,fullfile(fig_dir,'Fig6_Mean_Square_State_Zm.png'),'-dpng','-r600');
