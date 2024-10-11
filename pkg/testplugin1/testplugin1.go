package testplugin1

import (
	"context"
	"fmt"
	"strconv"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/klog/v2"
	"k8s.io/kubernetes/pkg/scheduler/framework"

	pluginConfig "sigs.k8s.io/scheduler-plugins/apis/config"

)

type TestPlugin1 struct {
	handle framework.handle
}

const (
	// Name is the name of the plugin used in the plugin registry and configurations.
	Name = "testplugin1"
	DefaultMissingLabelScore = 0
)

var _ = framework.TestPlugin1(&TestPlugin1{})

func (s *TestPlugin1) Name() string {
	return Name
}

func (s *TestPlugin1) Score(ctx context.Context, state *framework.CycleState, p *v1.Pod, nodeName string) (int64, *framework.Status) {
	nodeInfo, err := s.handle.SnapshotSharedLister().NodeInfos().Get(nodeName)
	if err != nil {
		return 0, framework.NewStatus(framework.Error, fmt.Sprintf("error getting node information: %s", err))
	}

	nodeLabels := nodeInfo.Node().Labels

	if val, ok := nodeLabels[LabelKey]; ok {
		scoreVal, err := strconv.ParseInt(val, 10, 64)
		if err != nil {
			klog.V(4).InfoS("unable to parse score value from node labels", LabelKey, "=", val)
			klog.V(4).InfoS("use the default score", DefaultMissingLabelScore, " for node with labels not convertable to int64!")
			return DefaultMissingLabelScore, nil
		}

		klog.Infof("[TestPlugin1] Label score for node %s is %s = %v", nodeName, LabelKey, scoreVal)

		return scoreVal, nil
	}

	return DefaultMissingLabelScore, nil
}

func (s *TestPlugin1) ScoreExtensions() framework.ScoreExtensions {
	return s
}

func (s *TestPlugin1) NormalizeScore(ctx context.Context, state *framework.CycleState, p *v1.Pod, scores framework.NodeScoreList) *framework.Status {
	var higherScore int64
	higherScore = framework.MinNodeScore
	for _, node := range scores {
		if higherScore < node.Score {
			higherScore = node.Score
		}
	}

	for i, node := range scores {
		scores[i].Score = node.Score * framework.MaxNodeScore / higherScore
	}

	klog.Infof("[TestPlugin1] Nodes final score: %v", scores)
	return nil
}

var LabelKey string

// New initializes a new plugin and returns it.
func New(obj runtime.Object, h framework.Handle) (framework.Plugin, error) {
	var args, ok = obj.(*pluginConfig.TestPlugin1Args)
	if !ok {
		return nil, fmt.Errorf("[TestPlugin1Args] want args to be of type TestPlugin1Args, got %T", obj)
	}

	klog.Infof("[TestPlugin1Args] args received. LabelKey: %s", args.LabelKey)
	LabelKey = args.LabelKey

	return &TestPlugin1{
		handle:     h,
	}, nil
}
