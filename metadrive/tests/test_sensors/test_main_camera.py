import pytest

from metadrive.envs.metadrive_env import MetaDriveEnv

blackbox_test_configs = dict(
    standard=dict(stack_size=3, width=64, height=32, norm_pixel=True),
    small=dict(stack_size=1, width=64, height=32, norm_pixel=False),
)


@pytest.mark.parametrize("config", list(blackbox_test_configs.values()), ids=list(blackbox_test_configs.keys()))
def test_main_camera(config, render=False):
    """
    Test the output shape of main camera. This can not make sure the correctness of rendered image but only for
    checking the shape of image output and image retrieve pipeline
    Args:
        config: test parameter
        render: render with cv2

    Returns: None

    """
    env = MetaDriveEnv(
        {
            "num_scenarios": 1,
            "traffic_density": 0.1,
            "show_terrain": False,
            "map": "S",
            "start_seed": 4,
            "window_size": (config["width"], config["height"]),
            "stack_size": config["stack_size"],
            "vehicle_config": dict(image_source="main_camera"),
            "sensors": {
                "main_camera": ()
            },
            "interface_panel": [],
            "image_observation": True,  # it is a switch telling metadrive to use rgb as observation
            "norm_pixel": config["norm_pixel"],  # clip rgb to range(0,1) instead of (0, 255)
        }
    )
    try:
        env.reset()
        import cv2
        import time
        start = time.time()
        for i in range(1, 10):
            o, r, tm, tc, info = env.step([0, 1])
            assert "LANE_SURFACE_STREET" in env.agent.contact_results
            assert env.observation_space.contains(o)
            # Reverse
            assert o["image"].shape == (config["height"], config["width"], 3, config["stack_size"])
            if render:
                cv2.imshow('img', o["image"][..., -1])
                cv2.waitKey(1)
        print("FPS:", 10 / (time.time() - start))
    finally:
        env.close()


if __name__ == '__main__':
    test_main_camera(config=blackbox_test_configs["small"], render=True)
