clear; clc; close all;%异步间歇自适应控制
rng(2026);
% 本版本未加入外部周期激励，仅通过调整复值振子模型参数，
% 使孤立系统保持非零持续振荡，并使受控网络同步到该轨迹。
set(0,'defaultAxesFontName','Times New Roman');
set(0,'defaultTextFontName','Times New Roman');
set(0,'defaultLegendInterpreter','none');
set(0,'defaultTextInterpreter','none');
set(0,'defaultAxesTickLabelInterpreter','none');
set(0,'defaultAxesFontSize',12);
set(0,'defaultTextFontSize',12);
set(0,'defaultLineLineWidth',1.5);
set(0,'defaultAxesLineWidth',1.2);
set(0,'defaultFigureColor','w');

fig_dir = fullfile(pwd,'complex_sync_theorem3_figures');
if ~exist(fig_dir,'dir')
    mkdir(fig_dir);
end

%% 基本参数
Tmax = 20;              % 仿真终止时间
h    = 0.002;           % Euler-Maruyama 步长
tau  = 0.10;            %% 实值时滞 tau
N0   = ceil(tau/h);     % 时滞对应的步数

time = -tau:h:Tmax;
Nt   = length(time);

Nnode = 13;             %% 节点数，根据有向图修改
Dim   = 2;              % 复值耦合振子状态 x_m(t)=(z_m^(1),z_m^(2))^T
YB    = 5;             %% Monte Carlo 样本数，生成轨迹图时改成1，均方图改成50

%% 异步间歇控制区间，满足条件 A2
% M_m(t1,t2) >= zeta_m^(2)*(t2-t1) - phi_0^m
% 其中 zeta_m^(2)=PJKZL(m)，phi_0^m=PHI0(m)>0
maxK   = ceil(Tmax/1.3) + 20;
TK     = zeros(Nnode,maxK);       % t_k^m
SK     = zeros(Nnode,maxK);       % s_k^m
Period = zeros(Nnode,1);          % 每个节点的间歇周期
Zeta   = zeros(Nnode,1);          % zeta_m^(2)，保留该变量供后续输出使用
PJKZL  = zeros(Nnode,1);          % 平均控制率下界
KZKD   = zeros(Nnode,1);          % 控制区间宽度
XXKD   = zeros(Nnode,1);          % 休息区间宽度
PHI0   = zeros(Nnode,1);          % 条件 A2 中的 phi_0^m
LastK  = zeros(Nnode,1);          % 每个节点的有效周期数

for m = 1:Nnode
    TK(m,1) = 0;

    % 周期随机取在 [1.3,1.7] 内，并离散到步长 h
    periodStep = fix(unifrnd(1.3,1.7)/h);
    periodStep = max(periodStep,1);
    Period(m)  = periodStep*h;

    % zeta_m^(2) 随机取在 [0.4,0.6] 内
    PJKZL(m) = unifrnd(0.4,0.6);%平均控制率zeta_m^(2)为04+0.6/2=0.5.
    Zeta(m)  = PJKZL(m);

    % 使用 ceil，保证离散后的实际控制率不低于 PJKZL(m)
    controlStep = ceil(periodStep*PJKZL(m));
    controlStep = min(max(controlStep,1),periodStep-1);
    KZKD(m) = controlStep*h;
    XXKD(m) = Period(m)-KZKD(m);

    % 取非零补偿常数 phi_0^m，并加入一个步长的离散裕量
    PHI0(m) = PJKZL(m)*XXKD(m) + h;

    k = 1;
    while TK(m,k) < Tmax && k < maxK-1
        SK(m,k)   = TK(m,k) + KZKD(m);
        TK(m,k+1) = TK(m,k) + Period(m);
        k = k + 1;
        if SK(m,k-1) >= Tmax
            break;
        end
    end
    LastK(m) = k-1;
end

Ictrl = zeros(Nnode,Nt);
for m = 1:Nnode
    k = 1;
    for it = 1:Nt
        if time(it) < 0
            continue;
        end
        if k <= LastK(m) && TK(m,k) <= time(it) && time(it) < SK(m,k)
            Ictrl(m,it) = 1;
        end
        if k <= LastK(m) && SK(m,k) > 0 && time(it)+1.5*h >= SK(m,k)
            k = k + 1;
        end
    end
end

%% 复值耦合振子参数，对应复值同步文件中的模型(3-1)--(3-3)
% z1' = z2 - delta1*z1 + coupling + noise
% z2' = (-delta2+delta1)*z2 + (delta2*delta1-delta1^2-1)*z1 - Y(z1(t-tau)) + coupling + noise

% 仅调整模型参数，不增加任何外部激励。
% 选择弱阻尼复参数，使孤立系统保持明显振荡；控制网络最终跟踪孤立系统。
% 因此孤立系统保持持续振荡，控制网络最终跟踪该非零振荡轨迹；
% 同步误差 e_m(t)=x_m(t)-y(t) 仍在控制作用下趋于零。
delta1 = 0.18 + 1.10i;          %% 复值坐标变换参数
delta2 = 0.08 + 0.95i;         %% 小阻尼参数，约等于 r_delay*tau
r_delay = 0.05 + 0.30i;                 %% 常值时滞反馈系数

% 复值噪声强度保持非零，但适当减小，避免噪声掩盖持续振荡轨迹
sigma1_now = 0.0030 + 0.0012i;
sigma1_tau = 0.0012 + 0.0005i;
sigma2_now = 0.0026 + 0.0010i;
sigma2_tau = 0.0010 + 0.0004i;

%% 为了使图1体现“同步到孤立系统轨迹”而不是“同步到零”
% 在孤立目标系统 y(t) 和控制网络 x_m(t) 中加入相同的外部周期激励。
% 这样同步误差系统不变，控制目标仍然是 e_m(t)=x_m(t)-y(t) -> 0；
% 但 y(t) 是非零振荡轨迹，因此图1会显示控制系统与孤立系统轨迹最终一致，而不是一起趋于0。
% drive_amp1 = 0.35 + 0.12i;
% drive_amp2 = 0.28 - 0.10i;
% drive_w1   = 1.20;
% drive_w2   = 0.85;

%% 单链接强连通有向环耦合网络，这里要根据条件和有向图修改
A = [ ...
0 1 0 0 0 0 0 0 0 0 0 0 0; ...
0 0 1 0 0 0 0 0 0 0 0 0 0; ...
0 0 0 1 0 0 0 0 0 0 0 0 0; ...
0 0 0 0 1 0 0 0 0 0 0 0 0; ...
0 0 0 0 0 1 0 0 0 0 0 0 0; ...
0 0 0 0 0 0 1 0 0 0 0 0 0; ...
0 0 0 0 0 0 0 1 0 0 0 0 0; ...
0 0 0 0 0 0 0 0 1 0 0 0 0; ...
0 0 0 0 0 0 0 0 0 1 0 0 0; ...
0 0 0 0 0 0 0 0 0 0 1 0 0; ...
0 0 0 0 0 0 0 0 0 0 0 1 0; ...
0 0 0 0 0 0 0 0 0 0 0 0 1; ...
1 0 0 0 0 0 0 0 0 0 0 0 0  ...
];

c_link = 0.03;
B = c_link*A;
Gamma = eye(Dim);

%% 自适应控制参数，与 th3.m 控制器形式一致，但作用于同步误差 e_m=x_m-y
p_adapt      = 2;
mu_adapt     = 0.020;%对应\psi_m
A0           = 1.30*ones(Nnode,Dim);
A_guard      = 80;

%% 定理3条件的数值型参数检查。这里需要自己验证
% 下面不是严格符号证明，而是给出仿真参数下的可验证量。
rowSum = zeros(Nnode,1);
for m = 1:Nnode
    rowSum(m) = sum(B(m,:))*norm(Gamma,2);
end
maxRowSum = max(rowSum);

% 对复值振子线性部分给一个保守的增长界估计
L_f_now = abs(delta1) + 1 + abs(-delta2+delta1) + abs(delta2*delta1-delta1^2-1);
L_f_tau = abs(r_delay);
L_g_now = abs(sigma1_now)^2 + abs(sigma2_now)^2;
L_g_tau = abs(sigma1_tau)^2 + abs(sigma2_tau)^2;
controlMargin = min(A0(:)) - L_f_now - L_g_now - 4*maxRowSum;
delayMargin   = controlMargin - (L_f_tau + L_g_tau);

%% 变量初始化，调图时这里可以变
X  = complex(zeros(YB,Dim,Nnode,Nt));   % 节点状态
Y  = complex(zeros(YB,Dim,Nt));         % 孤立目标系统/领导节点
E  = complex(zeros(YB,Dim,Nnode,Nt));   % 同步误差 e_m=x_m-y
U  = complex(zeros(YB,Dim,Nnode,Nt));   % 控制输入
Ad = zeros(Nnode,Dim,Nt);               % 自适应增益 A_m^(i)(t)

Ad(:,:,1:N0+1) = repmat(A0,[1 1 N0+1]);

dW = sqrt(h)*randn(YB,Nt);              % 复值系统中使用同一个实布朗运动 B(t)

for yb = 1:YB
    for it = 1:N0+1
        tt = time(it);
        Y(yb,1,it) = 0.35*exp(1i*(0.4*tt+0.2)) + 0.10*cos(2*tt);
        Y(yb,2,it) = 0.28*exp(1i*(0.3*tt-0.1)) + 0.08*sin(2*tt);
        for m = 1:Nnode
            X(yb,1,m,it) = Y(yb,1,it) + 0.85*cos(0.25*m) + 0.45i*sin(0.35*m) + 0.04*randn + 0.04i*randn;
            X(yb,2,m,it) = Y(yb,2,it) + 0.75*sin(0.30*m) - 0.35i*cos(0.20*m) + 0.04*randn + 0.04i*randn;
            E(yb,:,m,it) = squeeze(X(yb,:,m,it)).' - squeeze(Y(yb,:,it)).';
        end
    end
end

%% Euler-Maruyama 仿真
for yb = 1:YB
    for it = N0+1:Nt-1
        tt = time(it);

        % 更新自适应增益。与 th3.m 相同，只用第一条样本路径生成控制增益。
        if yb == 1
            for m = 1:Nnode
                e_now = squeeze(E(yb,:,m,it)).';
                for ii = 1:Dim
                    if Ictrl(m,it)==1
                        dA = exp(mu_adapt*tt)*(abs(e_now(ii))^p_adapt);
                        Ad(m,ii,it+1) = min(Ad(m,ii,it) + h*dA, A_guard);
                    else
                        Ad(m,ii,it+1) = Ad(m,ii,it);
                    end
                end
            end
        end

        % 目标系统 y(t)
        y_now = squeeze(Y(yb,:,it)).';
        y_tau = squeeze(Y(yb,:,it-N0)).';
        fy = zeros(Dim,1);
        gy = zeros(Dim,1);

        % 孤立目标系统：加入非零周期激励，使其保持非零振荡轨迹
%         drive1 = drive_amp1*sin(drive_w1*tt);
%         drive2 = drive_amp2*cos(drive_w2*tt);
        fy(1) = y_now(2) - delta1*y_now(1);
        fy(2) = (-delta2+delta1)*y_now(2) + (delta2*delta1-delta1^2-1)*y_now(1) - r_delay*y_tau(1);

        gy(1) = sigma1_now*y_now(1) + sigma1_tau*y_tau(1);
        gy(2) = sigma2_now*y_now(2) + sigma2_tau*y_tau(2);

        Y(yb,:,it+1) = y_now + h*fy + gy*dW(yb,it);

        for m = 1:Nnode
            x_now = squeeze(X(yb,:,m,it)).';
            x_tau = squeeze(X(yb,:,m,it-N0)).';
            e_now = x_now - y_now;

            fx = zeros(Dim,1);
            gx = zeros(Dim,1);
            % 控制系统加入与孤立目标系统完全相同的周期激励。
            % 因此图1显示的是 x_m(t) 与 y(t) 轨迹一致，而不是状态趋于0。
%             drive1 = drive_amp1*sin(drive_w1*tt);
%             drive2 = drive_amp2*cos(drive_w2*tt);
            fx(1) = x_now(2) - delta1*x_now(1);
            fx(2) = (-delta2+delta1)*x_now(2) + (delta2*delta1-delta1^2-1)*x_now(1) - r_delay*x_tau(1);

            gx(1) = sigma1_now*x_now(1) + sigma1_tau*x_tau(1);
            gx(2) = sigma2_now*x_now(2) + sigma2_tau*x_tau(2);

            coupling = zeros(Dim,1);
            for l = 1:Nnode
                if B(m,l) ~= 0
                    xl = squeeze(X(yb,:,l,it)).';
                    coupling = coupling + B(m,l)*(Gamma*(xl-x_now));
                end
            end

            if Ictrl(m,it)==1
                u = -[Ad(m,1,it)*e_now(1); Ad(m,2,it)*e_now(2)];
            else
                u = zeros(Dim,1);
            end
            U(yb,:,m,it) = u;

            X(yb,:,m,it+1) = x_now + h*(fx + coupling + u) + gx*dW(yb,it);
            E(yb,:,m,it+1) = squeeze(X(yb,:,m,it+1)).' - squeeze(Y(yb,:,it+1)).';
        end
    end
end

%% 计算均方同步误差
MSE1 = zeros(Nnode,Nt);
MSE2 = zeros(Nnode,Nt);
MSE  = zeros(Nnode,Nt);
for m = 1:Nnode
    for it = 1:Nt
        MSE1(m,it) = sum(abs(E(:,1,m,it)).^2)/YB;
        MSE2(m,it) = sum(abs(E(:,2,m,it)).^2)/YB;
        MSE(m,it)  = MSE1(m,it) + MSE2(m,it);
    end
end
MSE_mean = mean(MSE,1);

%% 数值检查输出
fprintf('\n===== Numerical simulation for complex-valued synchronization: Theorem 3 =====\n');
fprintf('Model: complex-valued coupled oscillator, x_m(t)=(z_m^(1)(t),z_m^(2)(t))^T.\n');
fprintf('Controller: I_m^(i)(t)=-A_m^(i)(t)(x_m^(i)(t)-y^(i)(t)) on intermittent intervals.\n');
fprintf('Adaptive law: dot A_m^(i)(t)=exp(mu*t)|x_m^(i)(t)-y^(i)(t)|^2.\n');
fprintf('Number of nodes N = %d, Monte Carlo samples = %d.\n',Nnode,YB);
fprintf('Delay tau = %.4f, step h = %.4f.\n',tau,h);
fprintf('delta1 = %.4f%+.4fi, delta2 = %.4f%+.4fi, r_delay = %.4f%+.4fi.\n', ...
    real(delta1),imag(delta1),real(delta2),imag(delta2),real(r_delay),imag(r_delay));
fprintf('Complex noise intensities: sigma1_now=%.4f%+.4fi, sigma1_tau=%.4f%+.4fi.\n',real(sigma1_now),imag(sigma1_now),real(sigma1_tau),imag(sigma1_tau));
fprintf('Complex noise intensities: sigma2_now=%.4f%+.4fi, sigma2_tau=%.4f%+.4fi.\n',real(sigma2_now),imag(sigma2_now),real(sigma2_tau),imag(sigma2_tau));
fprintf('Minimum control rate min zeta_m = %.4f.\n',min(Zeta));
fprintf('Maximum single-link row sum = %.4e.\n',maxRowSum);
fprintf('A conservative numerical margin = %.4e. Positive is desirable.\n',delayMargin);
fprintf('Initial mean-square synchronization error = %.4e.\n',MSE_mean(N0+1));
fprintf('Final mean-square synchronization error   = %.4e.\n',MSE_mean(end));
fprintf('Final adaptive gains: min %.4f, max %.4f.\n',min(min(Ad(:,:,end))),max(max(Ad(:,:,end))));

%% 作图数据
Tplot = time;
E1 = squeeze(E(1,1,:,:)).';      % Nt x Nnode
E2 = squeeze(E(1,2,:,:)).';      % Nt x Nnode
X1 = squeeze(X(1,1,:,:)).';
X2 = squeeze(X(1,2,:,:)).';
Y1 = squeeze(Y(1,1,:));
Y2 = squeeze(Y(1,2,:));

%% 图1(a)：x_m(t)=(z_m^{(1)}(t),z_m^{(2)}(t))^T 的实部轨迹
figure('Name','Real parts of x_m(t)','Units','centimeters','Position',[3 3 13 8]);
plot(Tplot,real(X1),'-','LineWidth',1.05); hold on;
plot(Tplot,real(X2),'--','LineWidth',1.05);
plot(Tplot,real(Y1),'k-','LineWidth',1.8);
plot(Tplot,real(Y2),'k--','LineWidth',1.8);
h1 = plot(nan,nan,'k-','LineWidth',1.5);
h2 = plot(nan,nan,'k--','LineWidth',1.5);
h3 = plot(nan,nan,'k:','LineWidth',1.8);
grid on; box on;
xlabel('Time (s)');
ylabel('Real parts');
title('Synchronization of controlled network and isolated target system');
legend([h1 h2 h3],{'Re\{z_m^{(1)}(t)\}','Re\{z_m^{(2)}(t)\}','Isolated target y(t)'},'Location','northeast');
set(gca,'LineWidth',1.2,'FontSize',12);
print(gcf,fullfile(fig_dir,'Fig1a_Real_xm_sync.png'),'-dpng','-r600');
print(gcf,fullfile(fig_dir,'Fig1a_Real_xm_sync.pdf'),'-dpdf','-painters');

%% 图1(b)：x_m(t)=(z_m^{(1)}(t),z_m^{(2)}(t))^T 的虚部轨迹
figure('Name','Imaginary parts of x_m(t)','Units','centimeters','Position',[3 3 13 8]);
plot(Tplot,imag(X1),'-','LineWidth',1.05); hold on;
plot(Tplot,imag(X2),'--','LineWidth',1.05);
plot(Tplot,imag(Y1),'k-','LineWidth',1.8);
plot(Tplot,imag(Y2),'k--','LineWidth',1.8);
h1 = plot(nan,nan,'k-','LineWidth',1.5);
h2 = plot(nan,nan,'k--','LineWidth',1.5);
h3 = plot(nan,nan,'k:','LineWidth',1.8);
grid on; box on;
xlabel('Time (s)');
ylabel('Imaginary parts');
title('Synchronization of controlled network and isolated target system');
legend([h1 h2 h3],{'Im\{z_m^{(1)}(t)\}','Im\{z_m^{(2)}(t)\}','Isolated target y(t)'},'Location','northeast');
set(gca,'LineWidth',1.2,'FontSize',12);
print(gcf,fullfile(fig_dir,'Fig1b_Imag_xm_sync.png'),'-dpng','-r600');
print(gcf,fullfile(fig_dir,'Fig1b_Imag_xm_sync.pdf'),'-dpdf','-painters');

% %% 图2：同步误差轨迹
% figure('Name','Synchronization errors','Units','centimeters','Position',[3 3 13 8]);
% plot(Tplot,abs(E1),'-','LineWidth',1.05); hold on;
% plot(Tplot,abs(E2),'--','LineWidth',1.05);
% h1 = plot(nan,nan,'k-','LineWidth',1.5);
% h2 = plot(nan,nan,'k--','LineWidth',1.5);
% grid on; box on;
% xlabel('Time (s)');
% ylabel('Synchronization error');
% legend([h1 h2],{'|e_m^{(1)}(t)|','|e_m^{(2)}(t)|'},'Location','northeast');
% set(gca,'LineWidth',1.2,'FontSize',12);
% print(gcf,fullfile(fig_dir,'Fig2_Sync_Errors.png'),'-dpng','-r600');
% print(gcf,fullfile(fig_dir,'Fig2_Sync_Errors.pdf'),'-dpdf','-painters');

%% 图3：均方同步误差
figure('Name','Mean-square synchronization errors','Units','centimeters','Position',[3 3 13 8]);
hold on;
for m = 1:Nnode
    plot(Tplot,MSE1(m,:),'-','LineWidth',1.05);
end
for m = 1:Nnode
    plot(Tplot,MSE2(m,:),'--','LineWidth',1.05);
end
h1 = plot(nan,nan,'k-','LineWidth',1.5);
h2 = plot(nan,nan,'k--','LineWidth',1.5);
grid on; box on;
xlabel('Time (s)');
ylabel('Mean-square error');
legend([h1 h2],{'E{|e_m^{(1)}(t)|^2}','E{|e_m^{(2)}(t)|^2}'},'Location','northeast');
set(gca,'LineWidth',1.2,'FontSize',12);
print(gcf,fullfile(fig_dir,'Fig3_Mean_Square_Sync_Error.png'),'-dpng','-r600');
print(gcf,fullfile(fig_dir,'Fig3_Mean_Square_Sync_Error.pdf'),'-dpdf','-painters');

%% 图4：自适应增益
figure('Name','Adaptive gains','Units','centimeters','Position',[3 3 12 8]);
plot(Tplot,squeeze(Ad(:,1,:)),'-','LineWidth',1.05); hold on;
plot(Tplot,squeeze(Ad(:,2,:)),'--','LineWidth',1.05);
h1 = plot(nan,nan,'k-','LineWidth',1.5);
h2 = plot(nan,nan,'k--','LineWidth',1.5);
grid on; box on;
xlabel('Time (s)');
ylabel('Adaptive gains');
legend([h1 h2],{'A_m^{(1)}(t)','A_m^{(2)}(t)'},'Location','northeast');
set(gca,'LineWidth',1.2,'FontSize',12);
print(gcf,fullfile(fig_dir,'Fig4_Adaptive_Gains.png'),'-dpng','-r600');
print(gcf,fullfile(fig_dir,'Fig4_Adaptive_Gains.pdf'),'-dpdf','-painters');

%% 图5：异步间歇控制区间
figure('Name','Asynchronous intermittent control intervals','Units','centimeters','Position',[3 3 12 8]);
imagesc(Tplot,1:Nnode,Ictrl); axis xy; colormap(gray);
xlabel('Time (s)');
ylabel('Node index');
title('Asynchronous intermittent control intervals');
set(gca,'LineWidth',1.2,'FontSize',12);
print(gcf,fullfile(fig_dir,'Fig5_Control_Intervals.png'),'-dpng','-r600');
print(gcf,fullfile(fig_dir,'Fig5_Control_Intervals.pdf'),'-dpdf','-painters');

fprintf('\nFigures have been exported to: %s\n',fig_dir);
